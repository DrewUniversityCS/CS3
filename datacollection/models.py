from django.db import models
from django.db.models import Count
from django.urls import reverse

from database.models.structural_models import ModelSet
from database.models.user_models import Student


class PreferenceForm(models.Model):
    """
    Keeps Track of preference form Open for a set.
    """
    course_set = models.ForeignKey(ModelSet, on_delete=models.CASCADE, related_name='course_form')
    student_set = models.ForeignKey(ModelSet, on_delete=models.CASCADE, related_name='student_form')
    name = models.CharField('Form Name', max_length=100)
    is_taking_responses = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.course_set}-{self.student_set} --> {self.is_taking_responses}'

    @property
    def total_students(self):
        return Student.objects.filter(sets__set=self.student_set).count()

    @property
    def response_entries(self):
        response_entries = PreferenceFormEntry.objects.filter(preference_form=self).values('email').annotate(
            n=Count('pk')).count()
        return response_entries, int(response_entries / self.total_students * 100.0)

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
