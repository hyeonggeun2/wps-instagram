from django.contrib.auth.models import AbstractUser
from django.db import models


# 추상유저 = 테이블로 만들어지지 않는다.
class User(AbstractUser):
    img_profile = models.ImageField('프로필이미지', blank=True, upload_to='users_profile/')
    name = models.CharField(max_length=30)