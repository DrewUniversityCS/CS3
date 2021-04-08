from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, ModelChoiceField

from database.forms import CrispyModelForm
from database.models.schedule_models import Course
from database.models.structural_models import ModelSet
from database.models.user_models import Student
from datacollection.models import PreferenceFormEntry, PreferenceForm


class PreferenceFormEntryForm(CrispyModelForm):
    preference_form = None

    class Meta:
        model = PreferenceFormEntry
        fields = ('student_name', 'email', 'courses')

    def __init__(self, preference_form, *args, **kwargs):
        super(PreferenceFormEntryForm, self).__init__(*args, **kwargs)
        self.preference_form = preference_form
        self.fields['courses'] = ModelMultipleChoiceField(
            queryset=Course.objects.filter(sets__set=preference_form.course_set), widget=CheckboxSelectMultiple
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Student.objects.filter(sets__set=self.preference_form.student_set, user__email=email).exists():
            raise ValidationError('You are not allowed to fill out the form!')
        return email


class PreferencesFormForm(CrispyModelForm):
    course_set = ModelChoiceField(
        queryset=ModelSet.objects.filter(obj_type__model='course').annotate(
            no_of_courses=Count('setmembership__course')
        ).exclude(Q(no_of_courses=0))
    )
    student_set = ModelChoiceField(
        queryset=ModelSet.objects.filter(obj_type__model='student').annotate(
            no_of_students=Count('setmembership__student'),
        ).exclude(Q(no_of_students=0))
    )

    class Meta:
        model = PreferenceForm
        fields = ('course_set', 'student_set', 'name',)
