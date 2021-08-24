from django.contrib import admin
import nested_admin
from .models import Exam, Question, Answer, ExamTaker, UserAnswer

class AnswerInline(nested_admin.NestedTabularInline):
 model = Answer
 extra = 4
 max_num = 4
class QuestionInline(nested_admin.NestedTabularInline):
 model = Question
 inline = [AnswerInline,]
 extra = 5

class ExamAdmin(nested_admin.NestedModelAdmin):
 inline = [QuestionInline,]

class UserAnswerInline(admin.TabularInline):
 model = UserAnswer

class ExamTakerAdmin(admin.ModelAdmin):
 inlines = [UserAnswerInline,]

admin.site.register(Exam,ExamAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ExamTaker, ExamTakerAdmin)
admin.site.register(UserAnswer)
