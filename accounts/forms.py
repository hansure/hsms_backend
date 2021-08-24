from django.contrib.auth import models
from django.db.models import fields
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserCreationForm(UserCreationForm):
 class Meta(UserCreationForm):
  model = UserAccount
  fields = ('username','email')

class UserChangeForm(UserChangeForm):
 class Meta:
  model = UserAccount
  fields = ('username','email')