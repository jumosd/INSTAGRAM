import os
import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from INSTAGRAM.settings import MEDIA_ROOT
from user.models import User
from .models import Feed, Reply, Like ,Bookmark
from uuid import uuid4

class Main(APIView):
    def get(self,request):
        email = request.session.get('email',None)
        
        feed_object_list = Feed.objects.all().order_by('-id') # 장고의 쿼리셋임  select * from content_feed;  와 같은동작을함
        
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.user_email).first()

            reply_objects_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_objects_list:
                reply_user = User.objects.filter(email=reply.email).first()
                reply_list.append({
                    'reply_content' : reply.reply_content,
                    'nickname' : reply_user.nickname,
                })

            like_count = Like.objects.filter(feed_id =feed.id, is_like = True).count()
            is_liked = Like.objects.filter(feed_id = feed.id, email = email , is_like = True).exists()
            is_bookmarked = Bookmark.objects.filter(feed_id = feed.id, email = email , is_bookmark = True).exists()

            like_objects = Like.objects.filter(feed_id = feed.id)
            like_name_list = []
            
            for name in like_objects:   
                like_name_list.append(name.nickname)

            print(like_name_list)    
                    

            try:
                # like_name = like_object.nickname
                # print(like_name)
                feed_list.append({
                              'feed_id': feed.id,
                              'content':feed.content,
                              'image':feed.image,
                              'profile_image':user.profile_image,
                              'user_nickname':user.nickname,
                              'like_count':like_count,
                              'user_email':user.email,
                              'reply_list':reply_list,
                              'is_liked' : is_liked,
                              'is_bookmarked' : is_bookmarked,
                              'like_name' : like_name_list[0:2]
                              })
            except :
                feed_list.append({
                              'feed_id': feed.id,
                              'content':feed.content,
                              'image':feed.image,
                              'profile_image':user.profile_image,
                              'user_nickname':user.nickname,
                              'like_count':like_count,
                              'user_email':user.email,
                              'reply_list':reply_list,
                              'is_liked' : is_liked,
                              'is_bookmarked' : is_bookmarked
                              })

            print('피드1')
        user = User.objects.filter(email=email).first()
        context ={
                    "feeds": feed_list,
                    "user": user
                }

        if email is None:
            return render(request, "user/login.html")

        if user is None:
            return render(request, "user/login.html")
        return render(request, "instagram/main.html",context=context,)
    
class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
         
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT,uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        email = request.session.get('email')
        image = uuid_name
        content = request.data.get("content")
        user_nickname = request.data.get("user_nickname")
        profile_image = request.data.get("profile_image")
        user_email = request.data.get("user_email")
        Feed.objects.create(content = content, image = image ,user_nickname = user_nickname, profile_image= profile_image, like_count = 0, user_email=user_email)
        return Response(status=200)
    
class Uploadreply(APIView):
    def post(self,request):

        feed_id = request.data.get('feed_id',None)
        print(feed_id)
        reply_content = request.data.get('reply_content',None)
        email = request.session.get('email',None)
        Reply.objects.create(
            feed_id = feed_id,
            reply_content = reply_content,
            email = email
        )
        return Response(status=200)


class ToggleLike(APIView):
    def post(self,request):
        email = request.session.get('email',None)
        feed_id = request.data.get('feed_id',None)
        is_like = request.data.get('is_like')

        is_user = Like.objects.filter(feed_id=feed_id, email=email).exists()
        _user = User.objects.filter(email=email).first()
        usernickname = _user.nickname
        print(email)

        if is_like == 'true' or is_like =='True':
            is_like = False
            update = Like.objects.get(feed_id=feed_id)
            update.delete()
        else: 
            if not is_user:
                Like.objects.create(
                    email = email,
                    feed_id = feed_id,
                    is_like = True,
                    nickname = usernickname
                )
              
        return Response(status = 200)

class ToggleBookmark(APIView):
    def post(self,request):
        email = request.session.get('email',None)
        feed_id = request.data.get('feed_id',None)
        is_bookmarked = request.data.get('is_bookmarked')
        user = Bookmark.objects.filter(feed_id=feed_id, email=email).exists()

        if is_bookmarked == 'true' or is_bookmarked =='True':
            is_bookmarked = False
            update = Bookmark.objects.get(feed_id=feed_id)
            update.delete()
        else: 
            if not user:
                Bookmark.objects.create(
                    email = email,
                    feed_id = feed_id,
                    is_bookmark = True
                )
              
        return Response(status = 200)
