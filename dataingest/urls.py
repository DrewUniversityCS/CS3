from django.urls import path
from django.views.generic import TemplateView

from dataingest import views

urlpatterns = [
    path("upload/",views.DataView.as_view())
]

app_name = 'pages'