from allauth.account.forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from datacollection.forms import PreferencesFormForm
from datacollection.models import PreferenceForm


class scheduleDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/schedule-documentation.html'

class DBDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/database-documentation.html'

class datasheetDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/datasheet-documentation.html'

class dbUpDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/databaseUp-documentation.html'

class studentDataDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/studentData-documentation.html'


