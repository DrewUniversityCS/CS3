from django.urls import path

from datacollection.views import PreferenceFormEntryView, OpenPreferenceSetView, OpenClosePreferenceSetFormView

urlpatterns = [
    path('student-form/<slug:form_id>/', PreferenceFormEntryView.as_view(), name='student_preference_form'),
    path('preference-set-form-open/', OpenPreferenceSetView.as_view(), name='preference_set_form_open'),
    path('preference-set-form/<slug:id>/<slug:type>/', OpenClosePreferenceSetFormView.as_view(),
         name='preference_set_form_open_close'),
]

app_name = 'datacollection'
