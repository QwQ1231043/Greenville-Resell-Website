from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    school_year_display = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "email", "is_student",
            "school_year", "school_year_display", "description",
            "avatar", "avatar_url", "groups", "user_permissions"
        ]
        extra_kwargs = {
            "password": {"write_only": True},  # 确保密码不会被序列化
        }

    def get_school_year_display(self, obj):
        return obj.get_school_year_display()

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
