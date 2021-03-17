from django.urls import path

from dataingest import views

urlpatterns = [
    path("upload/", views.upload, name="upload")
]

app_name = 'dataingest'
