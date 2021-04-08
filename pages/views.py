from collections import defaultdict

from allauth.account.forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView, FormView

from database.models.schedule_models import Section, Timeblock

from datacollection.forms import PreferencesFormForm
from datacollection.models import PreferenceForm
from pages.forms import CheckScheduleForm


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'open_new_preference_form': PreferencesFormForm(),
            'all_preference_forms': PreferenceForm.objects.all()
        })
        return context_data


class DocsView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/docs.html'


class StudentFormSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/student-form-success.html'


class GenerateScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/generate_schedule.html'


class CheckScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/check_schedule.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'check_schedule_form': CheckScheduleForm()
        })
        return context_data


class ScheduleRedirectView(LoginRequiredMixin, FormView):
    form_class = CheckScheduleForm

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('pages:schedule-view', kwargs={'schedule_id': form.cleaned_data['schedule'].id}))


class CrudView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/crud.html'


class InviteView(LoginRequiredMixin, FormView):
    form_class = SignupForm
    template_name = "account/new_admin_registration_form.html"
    success_url = reverse_lazy('pages:invite-success')

    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = "pages/final_schedule.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        sections = Section.objects.filter(schedule_id=kwargs.get('schedule_id'))
        section_time_block_dict = defaultdict(list)
        for section in  sections:
            section_time_block_dict[section.timeblock.id].append(section)

        timeblock_day_dict = defaultdict(dict)
        time_blocks = Timeblock.objects.all()

        for time_block in time_blocks:
            timeblock_day_dict[time_block.id] = self.generate_day_dict(section_time_block_dict[time_block.id])

        print(timeblock_day_dict)

        context_data.update({
            'time_blocks': time_blocks,
            'timeblock_day_dict': timeblock_day_dict,
            'day_list': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        })

        # section.timeblock.weekdays.monday == True



        # di[time_block.id]['monday']

        return context_data

    @classmethod
    def generate_day_dict(cls, sections):
        day_dict = defaultdict(list)
        for section in sections:
            if section.timeblock.weekdays.monday:
                day_dict['monday'].append(section)

            if section.timeblock.weekdays.tuesday:
                day_dict['tuesday'].append(section)

            if section.timeblock.weekdays.wednesday:
                day_dict['wednesday'].append(section)

            if section.timeblock.weekdays.thursday:
                day_dict['thursday'].append(section)

            if section.timeblock.weekdays.friday:
                day_dict['friday'].append(section)

        return day_dict
