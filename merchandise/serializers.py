from rest_framework import serializers
from .models import Merchandise, Merchandise_picture, Like


class MerchandisePictureSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()  # ✅ 让 Django 自动调用 `get_picture`

    class Meta:
        model = Merchandise_picture
        fields = ['id', 'picture']

    def get_picture(self, obj):
        """✅ 确保返回完整图片 URL，防止 `None` 或空数据"""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.picture.url)
        return obj.picture.url  # ✅ 确保仍然能返回 URL


class MerchandiseSerializer(serializers.ModelSerializer):
    pictures = MerchandisePictureSerializer(many=True, read_only=True,source='picture')  # ✅ 直接用 PictureSerializer
    username=serializers.CharField(source='user.username',read_only=True)
    useremail=serializers.CharField(source='user.email',read_only=True)
    userid=serializers.CharField(source='user.id',read_only=True)
    liked=serializers.SerializerMethodField()
    def get_liked(self, obj):
        """✅ 确保返回当前用户是否已 Like"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, merchandise=obj).exists()
        return False
    class Meta:
        model = Merchandise
        fields = ['id', 'name', 'price', 'description', 'pictures', 'is_negotiated', 'is_donation','username','useremail','userid','liked']
