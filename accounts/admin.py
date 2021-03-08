from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import BaseUserCreationForm, BaseUserChangeForm
from .models import BaseUser


class CustomUserAdmin(UserAdmin):
    add_form = BaseUserCreationForm
    form = BaseUserChangeForm
    model = BaseUser
    list_display = ['email', 'username', 'first_name', 'last_name']


admin.site.register(BaseUser, CustomUserAdmin)
