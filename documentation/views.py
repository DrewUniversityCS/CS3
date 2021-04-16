from allauth.account.forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from datacollection.forms import PreferencesFormForm
from datacollection.models import PreferenceForm


class HomeDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/home-documentation.html'


class DBDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/database-documentation.html'


class AdminDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/admin-documentation.html'




