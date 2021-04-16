from django.forms import forms, ModelChoiceField

from database.models.schedule_models import Schedule
from database.models.structural_models import ModelSet


class CheckScheduleForm(forms.Form):
    schedule = ModelChoiceField(queryset=Schedule.objects.all())
    preference_set = ModelChoiceField(queryset=ModelSet.objects.filter(obj_type__model='preference'))
