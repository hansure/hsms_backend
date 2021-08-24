from django.db import models
from django.contrib.auth.models import AbstractUser
import time
import os
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField

# def upload_to(instance, filename):
#     return 'posts/{filename}'.format(filename=filename)

# class UserAccountManager(BaseUserManager):
#     def create_user(self, username, email, password, phone, **extra_fields):
#         if not email:
#             raise ValueError('Users must have an email address')

#         elif not username:
#             raise ValueError('Users must have an username')

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#             phone = phone,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password, phone, **extra_fields):
#         user = self.create_user(
#             email=email,
#             username=username,
#             password=password,
#             phone=phone,
#             is_admin = True,
#         )
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         user.is_admin = True
#         user.save(using=self._db)
#         return user
class UserAccount(AbstractUser):
    # TYPE = (
    #     ('student', _('student')),
    #     ('teacher', _('teacher')),
    #     ('parent', _('parent'))
    # )
    role = models.CharField(max_length=10,default='student', verbose_name=_("User Type"))
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(max_length=255, unique=True, default="ATR/6558/09")
    first_name = models.CharField(max_length=255, default="Surafel")
    last_name = models.CharField(max_length=255, default="Melese")
    phone = PhoneField(blank=True, help_text='Contact phone number')

    # objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name', 'phone']


    def get_first_name(self):
        return self.first_name
    def get_last_name(self):
        return self.last_name

    def get_short_first_name(self):
        return self.first_name

    def get_short_last_name(self):
        return self.last_name

    def __str__(self):
        return self.username

