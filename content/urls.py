from django.urls import path
from .views import UploadFeed,Uploadreply,ToggleLike,ToggleBookmark

urlpatterns =[
    path('upload/', UploadFeed.as_view()),
    path('reply/', Uploadreply.as_view()),
    path('like/', ToggleLike.as_view()),
    path('bookmark/', ToggleBookmark.as_view())
]