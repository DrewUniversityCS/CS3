from django.urls import path
from django.views.generic import TemplateView

from .views import HomePageView, AboutPageView, InviteView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('invite/', InviteView.as_view(), name='invite'),
    path('invite-success/', TemplateView.as_view(template_name='account/newAdminRegistrationSuccess.html'), name='invite-success'),
    path('about/', AboutPageView.as_view(), name='about'),
]

app_name = 'pages'
