from django.urls import path,include
from . import views #UserViewSet

urlpatterns = [
    path('set/', views.create_dataset),
    path('train/', views.train_dataset),
    path('recognize/', views.face_recognizer
),
]
