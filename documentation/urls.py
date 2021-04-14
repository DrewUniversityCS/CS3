from django.urls import path
from django.views.generic import TemplateView

from documentation import views as page_views

urlpatterns = [
    path('home-documentation', page_views.HomeDocView.as_view(), name='home-documentation'),
    path('database-documentation', page_views.DBDocView.as_view(), name='database-documentation'),
    path('admin-documentation', page_views.AdminDocView.as_view(), name='admin-documentation'),
]

app_name = 'documentation'
