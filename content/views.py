from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed

class Main(APIView):
    def get(self,request):
        feed_list = Feed.objects.all() # 장고의 쿼리셋임  select * from content_feed;  와 같은동작을함

        return render(request, "instagram/main.html")