from django.urls import path

from database.views import department_crud

urlpatterns = [
    path('crud/departments', department_crud, name='department crud'),
]

app_name = 'database'
