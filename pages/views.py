from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from allauth.account.forms import SignupForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class InviteView(LoginRequiredMixin, FormView):
    form_class = SignupForm
    template_name = "account/newAdminRegistrationForm.html"
    success_url = reverse_lazy('pages:invite-success')

    def form_valid(self, form):

        form.save(self.request)
        return super().form_valid(form)
