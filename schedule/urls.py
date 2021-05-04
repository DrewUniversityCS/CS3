from django.urls import path

import schedule.views

urlpatterns = [
    path('check-schedule', schedule.views.CheckScheduleView.as_view(), name='check-schedule'),
    path('schedule/<slug:schedule_id>/<slug:preference_set_id>', schedule.views.ScheduleView.as_view(),
         name='schedule-table-view'),
    path('schedule-redirect', schedule.views.ScheduleRedirectView.as_view(), name='schedule-redirect'),
    path(
        'schedule/<slug:schedule_id>/<slug:preference_set_id>/<slug:section_id>',
        schedule.views.ScheduleSectionEditView.as_view(), name='schedule-section-edit'
    ),
    path(
        'notes/<slug:section_id>/<slug:color>', schedule.views.SectionNoteListView.as_view(), name='section-notes-list'
    ),
    path(
        'create-note/<slug:section_id>', schedule.views.SectionNoteFormView.as_view(), name='section-note-create'
    ),
]

app_name = 'schedule'
