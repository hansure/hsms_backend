from rest_framework import generics
from rest_framework.response import Response
from .models import Exam, Question,Category,Answer
from .serializers import ExamSerializer, RandomQuestionSerializer, AnswerSerializer, QuestionSerializer, QuestionSerializer,CategorySerializer
from rest_framework.views import APIView
from django.core import serializers
from rest_framework import viewsets
from rest_framework import status


class Category(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
class Answer(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class Exam(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()

class RandomQuestion(APIView):
    def get(self, request, format=None, **kwargs):
        question = Question.objects.filter(exam__title=kwargs['topic']).order_by('?')[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        post_data = request.data  # your post data will be here
        # serializers.get_deserializer(post_data)
        return Response(post_data)

class ExamQuestion(APIView):
    def get(self, request,topic, format=None, **kwargs):
        exam = Question.objects.filter(exam__title=kwargs['topic'])
        serializer = QuestionSerializer(exam, many=True)
        return Response(serializer.data)
    def post(self, request,topic, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)