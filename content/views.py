from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed

class Main(APIView):
    def get(self,request):
        feed_list = Feed.objects.all().order_by('-id') # 장고의 쿼리셋임  select * from content_feed;  와 같은동작을함
        
        context ={
            "feeds": feed_list
        }


        return render(request, "instagram/main.html",context=context)