from django.urls import path
from .views import get_chat_messages,send_message,get_unread_messages_count,get_recent_chats
urlpatterns = [
path('get_chat_messages/<int:user_id>/', get_chat_messages, name='get_chat_messages'),
    path('send_message/', send_message, name='send_message'),
    path('get_unread_messages_count/', get_unread_messages_count,name='get_unread_messages_count'),
    path('get_recent_chats/', get_recent_chats,name='get_recent_chats'),
 # ✅ 新增 API
]
