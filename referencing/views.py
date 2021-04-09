from allauth.account.forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from datacollection.forms import PreferencesFormForm
from datacollection.models import PreferenceForm


class ReferenceView(LoginRequiredMixin, TemplateView):
    template_name = 'referencing/home-ref.html'


class DBRefView(LoginRequiredMixin, TemplateView):
    template_name = 'referencing/db-ref.html'


class AdminRefView(LoginRequiredMixin, TemplateView):
    template_name = 'referencing/admin-ref.html'




