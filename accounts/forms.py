from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import BaseUser


class BaseUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = BaseUser
        fields = ('email', 'username', 'first_name', 'last_name')


class BaseUserChangeForm(UserChangeForm):
    class Meta:
        model = BaseUser
        fields = ('email', 'username', 'first_name', 'last_name')
