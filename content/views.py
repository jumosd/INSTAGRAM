import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from INSTAGRAM.settings import MEDIA_ROOT
from .models import Feed
from uuid import uuid4

class Main(APIView):
    def get(self,request):
        feed_list = Feed.objects.all().order_by('-id') # 장고의 쿼리셋임  select * from content_feed;  와 같은동작을함
        
        context ={
            "feeds": feed_list
        }
        return render(request, "instagram/main.html",context=context)
    


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES('file')
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT,uuid_name)


        image = request.data.get("image")
        content = request.data.get("content")
        user_id = request.data.get("user_id")
        profile_image = request.data.get("profile_image")
        Feed.objects.create(content = content, image = image, file= file ,user_id = user_id, profile_image= profile_image, like_count = 0)

        return Response(status=200)
