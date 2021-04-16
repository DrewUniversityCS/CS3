from django.urls import path

import schedule.views

urlpatterns = [
    path('check-schedule', schedule.views.CheckScheduleView.as_view(), name='check-schedule'),
    path('schedule/<slug:schedule_id>/<slug:preference_set_id>', schedule.views.ScheduleView.as_view(),
         name='schedule-table-view'),
    path('schedule-redirect', schedule.views.ScheduleRedirectView.as_view(), name='schedule-redirect'),
]

app_name = 'schedule'
