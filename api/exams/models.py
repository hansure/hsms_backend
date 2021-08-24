from django.db import models
from django.conf import settings
from django.db.models import query
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
class Exam(models.Model):
 name = models.CharField(max_length=200)
 description = models.CharField(max_length=70)
 image = models.ImageField()
 slug = models.SlugField(blank=True)
 roll_out = models.BooleanField(default=False)
 timestamp = models.DateTimeField(auto_now_add=True)
 class Meta:
  ordering = ['timestamp']
  verbose_name_plural="Exams"
 def __str__(self):
     return self.name

class Question(models.Model):
 exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
 label = models.CharField(max_length=100)
 order = models.IntegerField(default=0)
 def __str__(self):
    return self.label

class Answer(models.Model):
 question = models.ForeignKey(Question,null=True, on_delete=models.CASCADE)
 label = models.CharField(max_length=100)
 is_correct = models.BooleanField(default=False)
 def __str__(self):
    return self.label

class ExamTaker(models.Model):
 user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
 score = models.IntegerField(default=0)
 completed = models.BooleanField(default=False)
 date_finished = models.DateTimeField(auto_now = True)
 timestamp = models.DateTimeField(auto_now_add=True)
 def __str__(self):
    return self.user.username

class UserAnswer(models.Model):
 exam_taker = models.ForeignKey(ExamTaker, on_delete=models.CASCADE)
 question = models.ForeignKey(Question, on_delete=models.CASCADE)
 answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
 def __str__(self):
    return self.question.label

@receiver(pre_save, sender=Exam)
def slugify_name(sender, instance, *args, **kwargs):
 instance.slug = slugify(instance.name)