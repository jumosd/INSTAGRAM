from django.db import models



# Create your models here.
class Feed(models.Model):
    content = models.TextField() #글내용
    image = models.TextField() # 피드 이미지 
    profile_image = models.TextField() #프로필 사진
    user_nickname = models.TextField() # 글쓴이
    like_count = models.IntegerField() # 좋아요수
    user_email = models.EmailField()
    
class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()

class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_bookmark = models.BooleanField(default=True)