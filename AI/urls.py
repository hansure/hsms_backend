
from django.urls import path, include
from . import views
from . import camera

urlpatterns = [
    path('video_feed', camera.livefe, name='video_feed'),
    path('headposestimation/', views.headpose_estimation),
    path('data/', include('AI.faceRecognition.urls')),
    
]
