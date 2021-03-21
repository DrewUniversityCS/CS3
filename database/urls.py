from django.urls import path, re_path

from database.views import CrudView, CrudDeleteView, CrudUpdateView, CrudInspectView, DynamicModelSetCreateView, \
    DynamicModelSetUpdateView

urlpatterns = [
    path('crud/<slug:model>/', CrudView.as_view(), name='crud_model'),
    path('crud-inspect/<slug:model>/<slug:id>/', CrudInspectView.as_view(), name='crud_inspect'),
    path('crud-delete/<slug:model>/<slug:id>/', CrudDeleteView.as_view(), name='crud_delete'),
    path('crud-update/<slug:model>/<slug:id>/', CrudUpdateView.as_view(), name='crud_update'),
    path('set-crud/<slug:model>/', DynamicModelSetCreateView.as_view(), name='set_crud'),
    path('set-crud/<slug:model>/<slug:id>/', DynamicModelSetUpdateView.as_view(), name='set_crud_update'),
    path('set-crud/<slug:model>/<slug:id>/', DynamicModelSetUpdateView.as_view(), name='set_crud_inspect'),
    path('set-crud/<slug:model>/<slug:id>/', DynamicModelSetUpdateView.as_view(), name='set_crud_delete'),
]

app_name = 'database'
