from django.urls import path, re_path

from database.views import CrudView, CrudDeleteView, CrudUpdateView, CrudInspectView, DynamicModelSetCreateView, \
    DynamicModelSetUpdateView, DynamicModelSetInspectView, DynamicModelSetDeleteView, PreferenceFormEntryView, \
    OpenPreferenceSetView, OpenClosePrefernceSetFormView

urlpatterns = [
    path('crud/<slug:model>/', CrudView.as_view(), name='crud_model'),
    path('crud-inspect/<slug:model>/<slug:id>/', CrudInspectView.as_view(), name='crud_inspect'),
    path('crud-delete/<slug:model>/<slug:id>/', CrudDeleteView.as_view(), name='crud_delete'),
    path('crud-update/<slug:model>/<slug:id>/', CrudUpdateView.as_view(), name='crud_update'),

    path('set-crud/<slug:model>/', DynamicModelSetCreateView.as_view(), name='set_crud'),
    path('set-inspect/<slug:model>/<slug:id>/', DynamicModelSetInspectView.as_view(), name='set_crud_inspect'),
    path('set-delete/<slug:model>/<slug:id>/', DynamicModelSetDeleteView.as_view(), name='set_crud_delete'),
    path('set-update/<slug:model>/<slug:id>/', DynamicModelSetUpdateView.as_view(), name='set_crud_update'),

    path('student-form/<slug:form_id>/', PreferenceFormEntryView.as_view(), name='student_preference_form'),

    path('preference-set-form-open/', OpenPreferenceSetView.as_view(), name='preference_set_form_open'),
    path('preference-set-form/<slug:id>/<slug:type>/', OpenClosePrefernceSetFormView.as_view(),
         name='preference_set_form_open_close'),
]

app_name = 'database'
