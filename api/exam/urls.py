from django.urls import path,include
from .views import Exam, ExamQuestion,Category, RandomQuestion
from rest_framework.routers import DefaultRouter
app_name='exam'

router = DefaultRouter()
router.register('catagory', Category, basename='catagory')
router.register('answer', Category, basename='Answer')
router.register('ex', Exam, basename='Exam')
# router.register('question', Question, basename='Question')
urlpatterns = [
    path('', include(router.urls)),
    # path('question', ExamQuestion.as_view(),name='random'),
    path('r/<str:topic>/', RandomQuestion.as_view(), name='random'),
    path('q/<str:topic>/', ExamQuestion.as_view(), name='questions' ),
]