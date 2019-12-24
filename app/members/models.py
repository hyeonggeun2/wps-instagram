from django.contrib.auth.models import AbstractUser
from django.db import models


# 추상유저 = 테이블로 만들어지지 않는다.
class User(AbstractUser):
    """
    사용자 모델로 사용
    """
    pass