from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/home-documentation.html'


class DBDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/database-documentation.html'


class AdminDocView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/admin-documentation.html'




