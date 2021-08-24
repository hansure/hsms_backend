from django.contrib import admin
from .forms import UserCreationForm, UserChangeForm
from .models import UserAccount
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
 add_form = UserCreationForm
 form = UserChangeForm
 list_display = ('username','first_name','last_name','email', 'phone', 'role','is_active')
 list_filter = ('username','first_name','last_name','email', 'phone', 'role','is_active')
 fieldsets = (
  (None, {'fields': ('firs_name', 'last_name', 'username', 'email', 'password', 'phone','role')}),
   ('Permissions', {'fields': ('is_staff', 'is_active')})
 )
 search_fields = ('username',)
 ordering = ('username',)

admin.site.register(UserAccount, UserAdmin)
