from django.http import request, response
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from rest_framework import generics, permissions,status
from .serializers import ExamListSerializer,ExamDetailSerializer,MyExamListSerializer,UserAnswerSerializer,QuestionSerializer,ExamResultSerializer,ExamSerializer

from .models import Exam, ExamTaker, Question, UserAnswer, Answer
from rest_framework.response import Response


# class ExamAPI(generics.ListCreateAPIView):
#    def post(self, request, *args, **kwargs):
#       serializer = ExamSerializer(data=request.data)
#       if serializer.is_valid():
#         question = serializer.save()
#         serializer = ExamSerializer(question)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class QuestionsAPI(generics.ListCreateAPIView):
#    def post(self, request, *args, **kwargs):
#       serializer = QuestionSerializer(data=request.data)
#       if serializer.is_valid():
#         question = serializer.save()
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MyExamListAPI(generics.ListAPIView):
  permission_classes = [
    permissions.IsAuthenticated
  ]
  serializer_class = MyExamListSerializer
  def get_queryset(self, *args, **kwargs):
    queryset = Exam.objects.filter(examtaker__user=self.request.user)
    query = self.request.GET.get("q")
  
    if query:
      queryset = queryset.filter(Q(name__icontains=query)|Q(description__icontains=query)).distinct()
    
    return queryset
class ExamListAPI(generics.ListAPIView):
 serializer_class = ExamListSerializer
 permission_classes = [
    permissions.IsAuthenticated
  ]
 # If I want the exam as entry level the some we can exclude the current user quesryset = Exam.objects.filter(roll_out=True).exclude(examtaker__user=self.request.user)
 def get_queryset(self, *args, **kwargs):
  queryset = Exam.objects.filter(roll_out=True)
  query = self.request.GET.get("q")
  
  if query:
   queryset = queryset.filter(Q(name__icontains=query)|Q(description__icontains=query)).distinct()
  
  return queryset

class ExamDetailAPI(generics.RetrieveAPIView):
 serializer_class = ExamDetailSerializer
 permission_classes = [
    permissions.IsAuthenticated
  ]
 def get(self, *args, **kwargs):
  slug = self.kwargs["slug"]
  exam = get_object_or_404(Exam, slug = slug)
  last_question = None
  obj, created = ExamTaker.objects.get_or_create(user=self.request.user, exam=exam)
  if created:
   for question in Exam.objects.filter(exam=exam):
    UserAnswer.objects.create(exam_taker=obj, question=question)
  else:
   last_question = UserAnswer.objects.filter(exam_taker=obj, answer__isnull=False)
   if last_question.count() > 0:
    last_question = last_question.last().question.id
   else:
    last_question = None
  return Response({'exam': self.get_serializer(exam, context={'request': self.request}).data, 'last_question_id': last_question})

class SaveUserAnswer(generics.UpdateAPIView):
  serializer_class = UserAnswerSerializer
  permission_classes = [
    permissions.IsAuthenticated
  ]

  def patch(self, request, *args, **kwargs):
    examtaker_id = request.data['examtaker']
    # print('examtaker')
    question_id = request.data['question']
    answer_id = request.data['answer']

    examtaker = get_object_or_404(ExamTaker, id=examtaker_id)
    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(Answer, id=answer_id)

    if examtaker.completed:
      return Response({"message": "This exam is already completed. You con't answer any more questions"}, status = status.HTTP_412_PRECONDITION_FAILED)
    obj = get_object_or_404(UserAnswer, exam_taker=examtaker, question=question)
    obj.answer = answer
    obj.save()
    
    return Response(self.get_serializer(obj).data)

class SubmitExamAPI(generics.GenericAPIView):
  serializer_class = ExamResultSerializer
  permission_classes = [
    permissions.IsAuthenticated
  ]

  def post(self, request, *args, **kwargs):
    examtaker_id = request.data['examtaker']
    # print('examtaker')
    question_id = request.data['question']
    answer_id = request.data['answer']
    # slug = self.kwargs['slug']

    examtaker = get_object_or_404(ExamTaker, id=examtaker_id)
    question = get_object_or_404(Question, id=question_id)

    if examtaker.completed:
      return Response({"message": "This exam is already completed. You con't submit again!"}, status = status.HTTP_412_PRECONDITION_FAILED)
    if answer_id is not None:
      answer = get_object_or_404(Answer, id=answer_id)
      obj = get_object_or_404(UserAnswer, exam_taker=examtaker, question=question)
      obj.answer = answer
      obj.save()
    examtaker.completed = True
    correct_answers  = 0

    for user_answer in UserAnswer.objects.filter(exam_taker=examtaker):
      answer = Answer.objects.get(question=user_answer.question, is_correct=True)
      if user_answer.answer == answer:
        correct_answers += 1
    examtaker.score = int(correct_answers / examtaker.exam.questions_set.count()) * 100
    examtaker.save()

    return Response(self.get_serializer(examtaker).data)