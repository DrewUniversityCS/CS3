from django.urls import path
from django.views.generic import TemplateView

from pages import views as page_views
from .views import HomePageView, InviteView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('invite/', InviteView.as_view(), name='invite'),
    path('invite-success/', TemplateView.as_view(template_name='account/new_admin_registration_success.html'),
         name='invite-success'),
    path('docs', page_views.DocsView.as_view(), name='docs'),
    path('crud', page_views.CrudView.as_view(), name='crud'),
    path('student-form', page_views.StudentFormSuccessView.as_view(), name='student-form-success'),
]

app_name = 'pages'
