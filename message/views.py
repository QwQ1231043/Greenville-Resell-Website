from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q

User=get_user_model()
# ✅ 获取与某用户的聊天记录
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chat_messages(request, user_id):
    user = request.user
    print(user_id)
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    messages = Message.objects.filter(
        (Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user))
    ).order_by("timestamp")

    # ✅ 将所有收到的消息标记为已读
    unread_messages = messages.filter(receiver=user, is_read=False)
    unread_messages.update(is_read=True)

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

# ✅ 发送消息
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request):
    sender = request.user
    receiver_username = request.data.get("receiver")
    message_text = request.data.get("message")

    try:
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return Response({"error": "Receiver not found"}, status=404)

    message = Message.objects.create(sender=sender, receiver=receiver, message=message_text)
    return Response(MessageSerializer(message).data)

# ✅ 获取未读消息数量
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unread_messages_count(request):
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return Response({"unread_count": unread_count})


# ✅ 获取最近聊天用户（只显示最新一条）
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_recent_chats(request):
    user = request.user
    chat_partners = {}

    # 获取所有与自己有关的消息
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by("-timestamp")

    for message in messages:
        partner = message.sender if message.receiver == user else message.receiver
        if partner.id not in chat_partners:
            chat_partners[partner.id] = {
                "id": partner.id,
                "username": partner.username,
                "avatar": request.build_absolute_uri(partner.avatar.url) if partner.avatar else request.build_absolute_uri("/media/avatars/default.jpeg"),
                "latest_message": message.message,
                "timestamp": message.timestamp,
                "unread": Message.objects.filter(sender=partner, receiver=user, is_read=False).count(),
            }

    return Response(list(chat_partners.values()))



