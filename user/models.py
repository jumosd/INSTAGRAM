from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.
class User(AbstractBaseUser):
 
    profile_image = models.TextField(default="default.jpeg")
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)

    #커스텀 유저 를 생성시 유저네임필드가 있어야한다
    USERNAME_FIELD = 'nickname'
    #db에 저장될때에는 앱이름_클래스이름으로 db테이블에 생성된다
    #user_User 테이블이 생기지만  Meta클래스로 테이블 이름을 변경 할수있다.
    class Meta:
        db_table = "User"