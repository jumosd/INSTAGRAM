from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.urls import reverse
from .models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
class Join(APIView):
    def get(self,request):
        return render(request, "user/join.html")
    
    def post(self,request):
        #회원 가입기능
        email = request.data.get('email')
        name =  request.data.get('name')
        nickname = request.data.get('nickname')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if password1 == password2:
            password = make_password(password1)
            User.objects.create(email=email, name=name, nickname=nickname, password=password)
            return redirect('user:login')
        else:
            pass


class Login(APIView):
    def get(self,request):
        return render(request, "user/login.html")
    
    def post(self,request):
        #로그인 기능
        #리다이렉트 메인페이지
        return render(request, "user/login.html")