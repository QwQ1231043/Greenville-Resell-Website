from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Merchandise, Merchandise_picture, Like
from .serializers import MerchandiseSerializer

# ✅ 允许上传 multipart/form-data
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def merchandise_list_create(request):
    if request.method == 'GET':
        user=request.user
        print("Current User:", request.user)  # 应该是 user 不是 AnonymousUser
        print("Session Key:", request.session.session_key)  # 这个应该和数据库匹配
        merchandise = Merchandise.objects.all().order_by("-updated_on")
        serializer = MerchandiseSerializer(merchandise, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST' and request.user.is_authenticated:
        """✅ 创建商品 & 处理图片"""

        serializer = MerchandiseSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            merchandise = serializer.save(user=request.user)  # ✅ 让 Django 直接保存商品
            # ✅ 手动处理上传的图片
            images = request.FILES.getlist('pictures')
            for img in images:
                Merchandise_picture.objects.create(merchandise=merchandise, picture=img)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    print('g')
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def merchandiseDetail(request, merchandise_id):
    """✅ 获取商品详情"""
    merchandise = get_object_or_404(Merchandise, id=merchandise_id)

    data = {
        "id": merchandise.id,
        "name": merchandise.name,
        "description": merchandise.description,
        "price": merchandise.price,
        "is_negotiated": merchandise.is_negotiated,
        "is_donation": merchandise.is_donation,
        "seller": {
            "id": merchandise.user.id,
            'email': merchandise.user.email,
            "username": merchandise.user.username,
            "school_year": merchandise.user.school_year,
            'description': merchandise.description,
            "avatar": request.build_absolute_uri(merchandise.user.avatar.url) if merchandise.user.avatar else None,
        },
        "pictures": [{"id": pic.id, "picture": request.build_absolute_uri(pic.picture.url)} for pic in merchandise.picture.all()],
        "liked": merchandise.like_set.filter(user=request.user).exists(),
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST', 'PUT', 'DELETE','GET'])
@permission_classes([IsAuthenticated])  # ✅ 仅登录用户可修改或删除商品
def merchandise_detail(request, merchandise_id):
    """
    ✅ 创建、修改、删除商品
    """
    merchandise = get_object_or_404(Merchandise, id=merchandise_id)
    if request.method=='GET':
        serializer = MerchandiseSerializer(merchandise, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        """✅ 创建新商品"""
        serializer = MerchandiseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            merchandise = serializer.save(user=request.user)  # ✅ 让 Django 直接保存商品

            # ✅ 手动处理上传的图片
            images = request.FILES.getlist('pictures')
            for img in images:
                Merchandise_picture.objects.create(merchandise=merchandise, picture=img)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        """✅ 修改商品信息 & 重新上传图片"""
        if merchandise.user != request.user:
            return Response({"error": "你没有权限修改此商品"}, status=status.HTTP_403_FORBIDDEN)

        serializer = MerchandiseSerializer(merchandise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # ✅ 重新上传图片（删除旧图片，存储新图片）
            if 'pictures' in request.FILES:
                Merchandise_picture.objects.filter(merchandise=merchandise).delete()  # 删除旧图片
                images = request.FILES.getlist('pictures')
                for img in images:
                    Merchandise_picture.objects.create(merchandise=merchandise, picture=img)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """✅ 删除商品（仅允许所有者删除）"""
        if merchandise.user != request.user:
            return Response({"error": "你没有权限删除此商品"}, status=status.HTTP_403_FORBIDDEN)

        merchandise.delete()
        return Response({"message": "商品已删除"}, status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, merchandise_id):
    """✅ 处理 Like/Unlike"""
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        merchandise = Merchandise.objects.get(id=merchandise_id)
    except Merchandise.DoesNotExist:
        return Response({"error": "Merchandise not found"}, status=status.HTTP_404_NOT_FOUND)

    like, created = Like.objects.get_or_create(user=user, merchandise=merchandise)

    if created:
        return Response({"liked": True, "message": "Liked successfully"}, status=status.HTTP_201_CREATED)
    else:
        like.delete()
        return Response({"liked": False, "message": "Unliked successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_liked_merchandise(request):
    """✅ 获取用户喜欢的商品"""
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    # ✅ 通过 Like 关联表获取用户喜欢的商品
    liked_merchandise_ids = Like.objects.filter(user=user).values_list('merchandise_id', flat=True)
    liked_merchandise = Merchandise.objects.filter(id__in=liked_merchandise_ids)

    serializer = MerchandiseSerializer(liked_merchandise, many=True, context={'request': request})

    return Response(serializer.data, status=status.HTTP_200_OK)

def user_merchandise(request):
    """✅ 获取用户喜欢的商品"""
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    liked_merchandise = Merchandise.objects.filter(user=user)
    serializer = MerchandiseSerializer(liked_merchandise, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_merchandise(request):
    """
    ✅ 获取当前用户发布的所有商品
    """
    user = request.user
    merchandise = Merchandise.objects.filter(user=user).order_by("-updated_on")  # ✅ 获取当前用户发布的商品
    serializer = MerchandiseSerializer(merchandise, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ✅ 用户搜索 API
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_merchandise(request):
    query = request.GET.get("query", "")
    if not query:
        return Response([], status=200)

    merchandise = Merchandise.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )

    results = [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "is_negotiated": item.is_negotiated,
            "is_donation": item.is_donation,
            "username": item.user.username,
            "pictures": [{"picture": request.build_absolute_uri(pic.picture.url)} for pic in item.picture.all()],
            "liked": item.like_set.filter(user=request.user).exists(),
        }
        for item in merchandise[:10]  # 只返回前 10 个匹配商品
    ]

    return Response(results)