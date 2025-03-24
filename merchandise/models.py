from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  # 正确的导入方式

class Merchandise(models.Model):
    negotiate = {
        'negotiate': 'negotiate',
        'non-negotiate': 'non-negotiate',
    }
    is_negotiated = models.BooleanField(default=False)
    is_donation = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="merchandise")
    updated_on = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return self.title



class Merchandise_picture(models.Model):
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE, related_name="picture")
    picture = models.ImageField(upload_to="merchandise_pictures")

    def clean(self):
        picture_count = Merchandise_picture.objects.filter(merchandise=self.merchandise).count()
        if picture_count >= 5:
            raise ValidationError("One merchandise can only have 5 pictures.")

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'merchandise'], name='unique_user_merchandise_like')
        ]
