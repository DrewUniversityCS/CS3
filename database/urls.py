from django.urls import path

from database.views import CrudView, CrudDeleteView, CrudUpdateView, CrudInspectView, DynamicModelSetCreateView, \
    DynamicModelSetUpdateView, DynamicModelSetInspectView, DynamicModelSetDeleteView, CrudUsersView, CrudSetsView, CrudConstraintsView, \
    CrudSchedulingView
from datacollection.views import PreferenceFormEntryView, OpenPreferenceSetView, OpenClosePreferenceSetFormView

urlpatterns = [
    path('crud/users', CrudUsersView.as_view(), name='crud_users'),
    path('crud/sets', CrudSetsView.as_view(), name='crud_sets'),
    path('crud/constraints', CrudConstraintsView.as_view(), name='crud_constraints'),
    path('crud/scheduling', CrudSchedulingView.as_view(), name='crud_scheduling'),

    path('crud/<slug:model>/', CrudView.as_view(), name='crud_model'),
    path('crud-inspect/<slug:model>/<slug:id>/', CrudInspectView.as_view(), name='crud_inspect'),
    path('crud-delete/<slug:model>/<slug:id>/', CrudDeleteView.as_view(), name='crud_delete'),
    path('crud-update/<slug:model>/<slug:id>/', CrudUpdateView.as_view(), name='crud_update'),

    path('set-crud/<slug:model>/', DynamicModelSetCreateView.as_view(), name='set_crud'),
    path('set-inspect/<slug:model>/<slug:id>/', DynamicModelSetInspectView.as_view(), name='set_crud_inspect'),
    path('set-delete/<slug:model>/<slug:id>/', DynamicModelSetDeleteView.as_view(), name='set_crud_delete'),
    path('set-update/<slug:model>/<slug:id>/', DynamicModelSetUpdateView.as_view(), name='set_crud_update'),

]

app_name = 'database'
