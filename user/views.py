import os
import string
from datetime import time
import random
import time
from django.contrib.auth import logout, get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from Resell_Greenville import settings
from user.serializers import CustomUserSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


User=get_user_model()
@api_view(['GET'])
def default_page(request):
    x=1
    return JsonResponse({"message":'hello world'})

@api_view(['GET'])
def user_login(request):
    if request.user.is_authenticated:
        User = request.user
        serializer=CustomUserSerializer(User,context={'request':request})
        return Response({"login": True, "user":serializer.data})
    else:
        return Response({"login": False})

from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import CustomUser


@api_view(['POST','GET'])
@csrf_exempt
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({"error": "Email or password cannot be empty"}, status=400)
    user = authenticate(username=email, password=password)
    if user is None:
        return Response({"error": "Email or password is incorrect"}, status=400)
    # ✅ 确保 Django 正确存储 session
    login(request, user)
    print(user)
    print(request.user)
    print("User session:", request.session.session_key)  # 🔥 终端输出 session ID
    request.session.save()
    response = Response({
        "login": True,
        "user": {
            "email": user.email,
            "username": user.username
        }
    }, status=status.HTTP_200_OK)
    # ✅ 确保返回 sessionid
    response.set_cookie(
        key="sessionid",
        value=request.session.session_key,
        httponly=False,
        samesite="Lax",
    )
    return response


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def user_logout(request):
    print(request.user)
    response = Response({"message": "User logged out"}, status=status.HTTP_200_OK)
    response.delete_cookie("sessionid")  # 确保 Session 被清除
    response.delete_cookie("csrftoken")  # 确保 CSRF Token 也被清除
    logout(request)
    return response

User = get_user_model()


@api_view(['POST'])
def user_register(request):
    try:

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        description = request.data.get('description')
        school_year = request.data.get('school_year')
        verification_code = request.data.get('verification_code')

        is_student = email.endswith("@panthers.greenville.edu")

        # 🛑 验证字段是否存在
        if not username or not email or not password or not first_name or not last_name or not school_year or not verification_code:
            raise ValidationError("All fields are required!")

        # 🛑 检查用户名和邮箱是否已存在
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already taken")

        # 🛑 验证码验证
        stored_code = request.session.get('verification_code')
        if not stored_code or verification_code != stored_code:
            raise ValidationError("Invalid verification code, please check again")

        verification_code_time = request.session.get('verification_code_time')
        if not verification_code_time or (time.time() - float(verification_code_time) > 600):
            raise ValidationError("Verification code expired, please request a new one.")

        # ✅ 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            description=description,
            school_year=school_year,
            is_student=is_student
        )

        return Response({'message': 'User created successfully. You can now log in.'}, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  # ✅ 返回 JSON 错误

    except Exception as e:
        print("Unexpected error:", str(e))  # 🔥 让 Django 终端输出错误
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def user_verification(request):
    email = request.data.get('email')
    print(email)
    if not email:
        raise ValidationError("Email is required")

    # 生成六位验证码
    verification_code = "".join(random.sample(string.digits, 6))
    # 将验证码存储在 session 中
    request.session['verification_code'] = verification_code
    request.session['verification_code_time'] = time.time()
    request.session.modified = True  # 🔥 确保 Django 认为 session 发生了变化
    request.session.save()  # 🔥 强制 Django 立即保存 session
    # 发送邮件
    try:
        send_mail(
            'Your Verification Code',  # 邮件标题
            f'Your verification code is: {verification_code}',  # 邮件内容
            settings.DEFAULT_FROM_EMAIL,  # 发件人邮箱
            [email],  # 收件人邮箱
            fail_silently=False,  # 如果发送失败，抛出异常
        )
        return Response({'message': 'Verification code sent to your email.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'Failed to send verification code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        'id':user.id,
        "username": user.username,
        "email": user.email,
        "school_year": user.school_year,
        "description": user.description,
        "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None,
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    # 更新基本信息
    user.username = data.get("username", user.username)
    user.school_year = data.get("school_year", user.school_year)
    user.description = data.get("description", user.description)

    # 处理头像上传（删除旧头像）
    if "avatar" in request.FILES:
        avatar = request.FILES["avatar"]

        # 如果当前头像不是默认头像，则删除旧头像
        if user.avatar and user.avatar.name != "avatars/default.jpeg":
            old_avatar_path = os.path.join(settings.MEDIA_ROOT, user.avatar.name)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)  # 删除旧头像文件

        # 保存新头像
        file_path = f"avatars/{user.id}_{avatar.name}"
        default_storage.save(file_path, ContentFile(avatar.read()))
        user.avatar = file_path
    user.save()
    return Response({"message": "✅ Profile updated successfully!"})

# ✅ 用户搜索 API
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get("query", "")
    if not query:
        return Response([], status=200)

    users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)

    results = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else request.build_absolute_uri(
                "/media/avatars/default.jpeg"),
        }
        for user in users[:10]  # 只返回前 10 个匹配用户
    ]

    return Response(results)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_by_username(request):
    username = request.query_params.get("username")

    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        user = User.objects.get(username=username)
        return Response({
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar.url if user.avatar else None,
        })
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
@api_view(['POST'])
def verify_and_reset_password(request):
    """✅ 验证验证码 + 重置密码"""

    # 🛠️ 获取 session 里的验证码和 email
    email = request.data.get('email')
    stored_code = request.session.get('verification_code')
    code_time = request.session.get('verification_code_time')

    # 🛠️ 获取前端输入的验证码 & 新密码
    user_code = request.data.get('code')
    new_password = request.data.get('new_password')

    # ✅ 打印日志查看数据是否正确
    print(f"Session Data: email={email}, stored_code={stored_code}, code_time={code_time}")
    print(f"User Input: code={user_code}, new_password={new_password}")

    print(time.time() - code_time > 300)
    # 2️⃣ **检查验证码是否超时（5分钟）**
    if time.time() - code_time > 300:
        return Response({'message': 'Verification code expired'}, status=status.HTTP_400_BAD_REQUEST)

    # 3️⃣ **检查验证码是否匹配**
    if str(user_code) != str(stored_code):
        return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

    # 4️⃣ **确保密码长度符合要求**
    if not new_password:
        return Response({'message': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        # ✅ 清除 session 数据
        del request.session['verification_code']

        del request.session['verification_code_time']

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

