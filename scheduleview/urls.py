from django.urls import path

import scheduleview.views

urlpatterns = [
    path('check-schedule', scheduleview.views.CheckScheduleView.as_view(), name='check-schedule'),
    path('schedule/<slug:schedule_id>/<slug:preference_set_id>', scheduleview.views.ScheduleView.as_view(), name='schedule-view'),
    path('schedule-redirect', scheduleview.views.ScheduleRedirectView.as_view(), name='schedule-redirect'),
]

app_name = 'scheduleview'
