from django.urls import path
from django.views.generic import TemplateView

from referencing import views as page_views

urlpatterns = [
    path('home-ref', page_views.ReferenceView.as_view(), name='home-ref'),
    path('db-ref', page_views.DBRefView.as_view(), name='db-ref'),
    path('admin-ref', page_views.AdminRefView.as_view(), name='admin-ref'),
]

app_name = 'referencing'
