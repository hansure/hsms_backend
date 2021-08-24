
from django.urls import path, include
from rest_framework.authtoken import views
#from . views import article_list,article_details
#from .views import ArticleList,ArticleDetails


urlpatterns = [
    path('Info/', include('api.articles.urls')),
    path('exams/', include('api.exam.urls')),
    path('entrance/', include('api.exams.urls')),
    # path('articles/', ArticleList.as_view()),
    # path('articles/<int:id>/', ArticleDetails.as_view()),
    #path('articles/', article_list),
    #path('articles/<int:pk>/', article_details),
]
