from django.urls import path

from documentation import views as page_views

urlpatterns = [
    path('schedule-documentation', page_views.ScheduleDocView.as_view(), name='schedule-documentation'),
    path('database-documentation', page_views.DBDocView.as_view(), name='database-documentation'),
    path('datasheet-documentation', page_views.DatasheetDocView.as_view(), name='datasheet-documentation'),
    path('databaseUp-documentation', page_views.DbUpDocView.as_view(), name='databaseUp-documentation'),
    path('studentData-documentation', page_views.StudentDataDocView.as_view(), name='studentData-documentation'),
]

app_name = 'documentation'
