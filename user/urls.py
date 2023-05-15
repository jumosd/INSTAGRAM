from django.urls.conf import path, include
from .views import Join, Login, LogOut, Profile

app_name="user"


urlpatterns =[
    path('join/', Join.as_view(), name="join"),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
]