import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from INSTAGRAM.settings import MEDIA_ROOT
from user.models import User
from .models import Feed
from uuid import uuid4

class Main(APIView):
    def get(self,request):
        feed_object_list = Feed.objects.all().order_by('-id') # 장고의 쿼리셋임  select * from content_feed;  와 같은동작을함
        
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.user_email).first()
            feed_list.append({'content':feed.content,
                              'image':feed.image,
                              'profile_image':user.profile_image,
                              'user_nickname':user.nickname,
                              'like_count':feed.like_count,
                              'user_email':user.email,
                              }
                             )

        email = request.session.get('email',None)
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

        image = uuid_name
        content = request.data.get("content")
        user_nickname = request.data.get("user_nickname")
        profile_image = request.data.get("profile_image")
        user_email = request.data.get("user_email")
        Feed.objects.create(content = content, image = image ,user_nickname = user_nickname, profile_image= profile_image, like_count = 0, user_email=user_email)

        return Response(status=200)