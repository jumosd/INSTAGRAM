from django.urls import path
from .views import UploadFeed,Uploadreply

urlpatterns =[
    path('upload/', UploadFeed.as_view()),
    path('reply/', Uploadreply.as_view())
]