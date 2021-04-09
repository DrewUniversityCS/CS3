from django.forms import ModelChoiceField, forms

from database.models.schedule_models import Schedule


class CheckScheduleForm(forms.Form):
    schedule = ModelChoiceField(queryset=Schedule.objects.all())
