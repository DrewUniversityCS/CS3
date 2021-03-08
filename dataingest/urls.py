from django.urls import path

from dataingest import views

urlpatterns = [
    path("upload/", views.DataView.as_view())
]

app_name = 'dataingest'
