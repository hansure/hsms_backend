from django.db.models import fields
from rest_framework import serializers
from .models import Exam, ExamTaker, Question, Answer,UserAnswer

class MyExamListSerializer(serializers.ModelSerializer):
 completed = serializers.SerializerMethodField()
 questions_count = serializers.SerializerMethodField()
 progress = serializers.SerializerMethodField()
 score = serializers.SerializerMethodField()
 class  Meta:
  model= Exam
  fields = ["id", "name", "description", "image","slug", "questions_count", "completed", "score", "progress"]
  read_only_fields = ["questions_count", "completed","score", "progress"]
 def get_questions_count(self, obj):
   return obj.question_set.all().count()
 def get_questions_count(self, obj):
  return obj.question_set.all().count()
 def get_completed(self, obj):
  try:
    examtaker = ExamTaker.objects.get(user=self.context['request'].user, exam=obj)
    return examtaker.completed
  except ExamTaker.DoesNotExist:
    return None
 def get_progress(self, obj):
  try:
    examtaker = ExamTaker.objects.get(user=self.context['request'].user, exam=obj)
    if examtaker.completed == False:
      questions_answered = UserAnswer.objects.filter(exam_taker=examtaker , answer__isnull=False).count() 
      total_questions = obj.question_set.all().count()
      return int(questions_answered / total_questions)
    return None
  except ExamTaker.DoesNotExist:
    return None
 def get_score(self, obj):
  try:
    examtaker = ExamTaker.objects.get(user=self.context['request'].user, exam=obj)
    if examtaker.completed == True:
      return examtaker.score
    return None
  except ExamTaker.DoesNotExist:
    return None


class ExamListSerializer(serializers.ModelSerializer):
 questions_count = serializers.SerializerMethodField()
 class Meta:
  model = Exam
  fields = ["id", "name", "description","image", "slug","questions_count"]
  read_only_fields = ["questions_count"]
 
 def get_questions_count(self, obj):
  return obj.question_set.all().count()
 def get_completed(self, obj):
  try:
    examtaker = ExamTaker.objects.get(user=self.context['request'].user, exam=obj)
    return examtaker.completed
  except ExamTaker.DoesNotExist:
    return None
 def get_progress(self, obj):
  try:
    examtaker = ExamTaker.objects.get(user=self.context['request'].user, exam=obj)
    if examtaker.completed == False:
      questions_answered = UserAnswer.objects.filter(exam_taker=examtaker , answer__isnull=False).count() 
      total_questions = obj.question_set.all().count()
      return int(questions_answered / total_questions)
    return None
  except ExamTaker.DoesNotExist:
    return None
 def get_score(self, obj):
  try:
    examtaker = ExamTaker.objects.get(user=self.context['request'].user, exam=obj)
    if examtaker.completed == True:
      return examtaker.score
    return None
  except ExamTaker.DoesNotExist:
    return None

class AnswerSerializer(serializers.ModelSerializer):
 class  Meta:
  model= Answer
  fields = ["id", "question", "label", "is_correct"]

class ExamSerializer(serializers.ModelSerializer):
 class Meta:
  model = Exam
  fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
 answer_set = AnswerSerializer(many = True)
 class Meta:
  model = Question
  fields = "__all__"

class UserAnswerSerializer(serializers.ModelSerializer):
 class Meta:
  model = UserAnswer
  fields = "__all__"
class ExamTakerSerializer(serializers.ModelSerializer):
 useranswer_set = UserAnswerSerializer(many=True)
 class Meta:
  model = ExamTaker
  fields = "__all__"

class ExamDetailSerializer(serializers.ModelSerializer):
 examtakers_set = serializers.SerializerMethodField()
 question_set = QuestionSerializer(many=True)
 class Meta:
  model = Exam
  fields = "__all__"
 
 def get_examtakers_set(self, obj):
  try:
   exam_taker = ExamTaker.objects.get(user=self.context['request'].user, exam=obj)
   serializer = ExamTakerSerializer(exam_taker)
   return serializer.data
  except ExamTaker.DoesNotExist:
   return None

class ExamResultSerializer(serializers.ModelSerializer):
  examtaker_set = serializers.SerializerMethodField()
  question_set = QuestionSerializer(many=True)

  class Meta:
    model = Exam
    fields = "__all__"

  def get_examtaker_set(self, obj):
    try:
      examtaker = ExamTaker.objects.get.get(user=self.context['request'].use, exam=obj)
      serializer = ExamTakerSerializer(examtaker)
      return serializer.data

    except  ExamTaker.DoesNotExist:
      return None