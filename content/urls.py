from django.urls import path
from .views import UploadFeed,Uploadreply,ToggleLike

urlpatterns =[
    path('upload/', UploadFeed.as_view()),
    path('reply/', Uploadreply.as_view()),
    path('like/', ToggleLike.as_view())
]