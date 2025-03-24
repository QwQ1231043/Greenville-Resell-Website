from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """允许使用 email 作为用户名登录"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # ✅ 通过 email 查找用户
        except User.DoesNotExist:
            return None
        if user.check_password(password):  # ✅ Django 自动验证哈希密码
            return user
        return None
