from django.db import models

# Create your models here.
from django.db.models import Count
from django.urls import reverse

from database.models.structural_models import ModelSet


class PreferenceForm(models.Model):
    """
    Keeps Track of preference form Open for a set.
    """
    set = models.OneToOneField(ModelSet, on_delete=models.CASCADE, related_name='preference_form')
    is_taking_responses = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.set} --> {self.is_taking_responses}'

    @property
    def total_students(self):
        from database.models.user_models import Student
        return Student.objects.filter(sets__set=self.set).count()

    @property
    def response_entries(self):
        response_entries = PreferenceFormEntry.objects.filter(preference_form=self).values('email').annotate(
            n=Count('pk')).count()
        print(PreferenceFormEntry.objects.filter(preference_form=self).values('email').annotate(n=Count('pk')))
        return response_entries, response_entries / self.total_students * 100.0

    @property
    def no_response_entries(self):
        return self.total_students - self.response_entries[0], 100 - self.response_entries[1]

    @property
    def form_link(self):
        return reverse('datacollection:student_preference_form', kwargs={'form_id': self.id})


class PreferenceFormEntry(models.Model):
    """
    Keeps Student preference entries
    """
    preference_form = models.ForeignKey(PreferenceForm, on_delete=models.CASCADE, related_name='entries')
    student_name = models.CharField('Student Name', max_length=100)
    email = models.EmailField('Student Email')
    courses = models.ManyToManyField('database.Course')

    def __str__(self):
        return f'{self.student_name}({self.email}) - {self.preference_form.set}'
