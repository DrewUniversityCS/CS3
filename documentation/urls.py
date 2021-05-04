from django.urls import path
from django.views.generic import TemplateView

from documentation import views as page_views

urlpatterns = [
    path('schedule-documentation', page_views.scheduleDocView.as_view(), name='schedule-documentation'),
    path('database-documentation', page_views.DBDocView.as_view(), name='database-documentation'),
    path('datasheet-documentation', page_views.datasheetDocView.as_view(), name='datasheet-documentation'),
    path('databaseUp-documentation', page_views.dbUpDocView.as_view(), name='databaseUp-documentation'),
    path('studentData-documentation', page_views.studentDataDocView.as_view(), name='studentData-documentation'),
]

app_name = 'documentation'
