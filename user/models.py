from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.
class User(AbstractBaseUser):
    """
    프로필사진 =텍스트필드(텍스트필드는 길이무제한)
    닉네임 = 캐릭터필드 24자
    이름 =캐릭터필드 24자
    이메일 =이메일필드
    비번 = 원래있던거
    """
    profile_image = models.TextField()
    nickname = models.CharField(max_length=24)
    name = models.CharField(max_length=24)
    email = models.EmailField()
    
    #db에 저장될때에는 앱이름_클래스이름으로 db테이블에 생성된다
    #user_User 테이블이 생기지만  Meta클래스로 테이블 이름을 변경 할수있다.
    class Meta:
        db_table = "User"