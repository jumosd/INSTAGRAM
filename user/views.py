from django.shortcuts import render, redirect
from rest_framework.views import APIView,Response
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
            return Response(status=200)
        
class Login(APIView):
    def get(self,request):
        return render(request, "user/login.html")
    
    def post(self,request):
        #로그인 기능
        email =  request.data.get('email',None)
        password =  request.data.get('password',None)
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response(status=400,data=dict(massage="로그인 정보가 잘못되었습니다."))

        if user.check_password(password):
            #로그인을 했다 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400,data=dict(massage="로그인 정보가 잘못되었습니다."))

class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        print("로그아웃")
        
        
        return redirect('home')
    
class Profile(APIView):
    def get(self, request):
        email = request.session.get('email')
        user = User.objects.filter(email=email).first()
        context={
            'user': user
        }
        return render(request,'user/profile.html', context=context)
    

    def post(self, request):        
        email = request.session.get('email')
        user = User.objects.filter(email=email)
