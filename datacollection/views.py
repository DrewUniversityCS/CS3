from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView

from database.models.user_models import Student
from datacollection.forms import PreferencesFormForm, PreferenceFormEntryForm
from datacollection.models import PreferenceForm, PreferenceFormEntry


class PreferenceFormEntryView(LoginRequiredMixin, FormView):
    template_name = 'pages/student-form.html'
    success_url = reverse_lazy('pages:student-form-success')
    preference_form = None

    def dispatch(self, request, *args, **kwargs):
        self.preference_form = get_object_or_404(PreferenceForm, pk=self.kwargs.get('form_id'))
        if not self.preference_form.is_taking_responses:
            raise Http404
        return super().dispatch(request, args, kwargs)

    def get_form(self, form_class=None):
        return PreferenceFormEntryForm(self.preference_form, **self.get_form_kwargs())

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.preference_form = self.preference_form
        with transaction.atomic():
            entry.save()
            entry_to_course_link = []
            for course in form.cleaned_data['courses']:
                preference_entry_course = PreferenceFormEntry.courses.through(
                    preferenceformentry_id=entry.id, course_id=course.id
                )
                entry_to_course_link.append(preference_entry_course)

            PreferenceFormEntry.courses.through.objects.bulk_create(entry_to_course_link, batch_size=7000)
        return super().form_valid(form)


class OpenPreferenceSetView(LoginRequiredMixin, FormView):
    form_class = PreferencesFormForm
    success_url = reverse_lazy('pages:home')

    def form_valid(self, form):
        preference_form = form.save()
        email_ids = Student.objects.filter(sets__set=preference_form.student_set).values_list('user__email', flat=True)
        send_mail('Preference Form',
                  f'Fill Course preferences for {preference_form.name} here:\n\nhttp://{settings.DOMAIN}{preference_form.form_link}\n\nTeam CS3',
                  settings.FROM_EMAIL, email_ids, fail_silently=False)
        return super().form_valid(form)


class OpenClosePreferenceSetFormView(LoginRequiredMixin, View):
    template_name = 'pages/home.html'

    def post(self, request, *args, **kwargs):
        update = {}
        if kwargs.get('type') == 'remove':
            update['is_active'] = False
        elif kwargs.get('type') == 'open':
            update['is_taking_responses'] = True
        elif kwargs.get('type') == 'close':
            update['is_taking_responses'] = False
        PreferenceForm.objects.filter(id=kwargs.get('id')).update(**update)
        return HttpResponseRedirect(reverse('pages:home'))
