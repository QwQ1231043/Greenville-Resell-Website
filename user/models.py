
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    SchoolYear = {
        "Freshmen": "Freshmen",
        "Sophomore": "Sophomore",
        "Junior": "Junior",
        "Senior": "Senior",
    }
    is_student=models.BooleanField(default=False)
    email = models.EmailField(unique=True)  # email 字段唯一
    username = models.CharField(max_length=50, unique=True)
    school_year = models.CharField(choices=SchoolYear.items(), max_length=10)
    description = models.TextField(null=True, blank=True, default="This user is too lazy to leave anything behind")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default="avatars/default.jpeg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # 这里设置了 related_name，避免冲突
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # 设置 related_name，避免冲突
        blank=True
    )
