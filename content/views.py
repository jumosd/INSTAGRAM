import os
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
                user = User.objects.filter(email=reply.email).first()
                reply_list.append({
                    'reply_content' : reply.reply_content,
                    'nickname' : user.nickname,

                })
            like_count = Like.objects.filter(feed_id =feed.id, is_like = True).count()
            is_liked = Like.objects.filter(feed_id = feed.id, email = email , is_like = True).exists()
            print(is_liked)
            feed_list.append({
                              'feed_id': feed.id,
                              'content':feed.content,
                              'image':feed.image,
                              'profile_image':user.profile_image,
                              'user_nickname':user.nickname,
                              'like_count':like_count,
                              'user_email':user.email,
                              'reply_list':reply_list,
                              'is_liked' : is_liked
                              }
                             )


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
        user = User.objects.filter(email=email).first()
        
        
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
        # user = Like.objects.filter(email=email).first()
        # print("user")
        if is_like == 'true' or is_like =='True':
            is_like = False
            update = Like.objects.get(feed_id=feed_id)
            update.is_like = is_like
            update.save()
            
        else: 
            if user == None:
                Like.objects.create(
                    email = email,
                    feed_id = feed_id,
                    is_like = True
                )
            else:
                is_like = True
                update = Like.objects.get(feed_id=feed_id)
                update.is_like = is_like
                update.save()

        
        return Response(status = 200)

