from django.urls import path, re_path
# from django.urls.resolvers import URLPattern
from .views import MyExamListAPI, ExamListAPI, ExamDetailAPI, SaveUserAnswer, SubmitExamAPI
# QuestionsAPI,ExamAPI


urlpatterns = [
 path("exams/", ExamListAPI.as_view()),
 path("my-exams/", MyExamListAPI.as_view()),
 # path("question/", QuestionsAPI.as_view()),path("add_exams/", ExamAPI.as_view()),
 path("save_answer/", SaveUserAnswer.as_view()),
 re_path(r"exams/(?P<slug>[-\w]+)/$", ExamDetailAPI.as_view()),
 re_path(r"^exams/(?P<slug>[-\w]+)/submit/$", SubmitExamAPI.as_view())
]