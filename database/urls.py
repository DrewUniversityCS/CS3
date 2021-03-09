from django.urls import path

from database.views import CrudView, CrudDeleteView, CrudUpdateView, CrudInspectView

urlpatterns = [
    path('crud/<slug:model>/', CrudView.as_view(), name='crud_model'),
    path('crud-inspect/<slug:model>/<slug:id>/', CrudInspectView.as_view(), name='crud_inspect'),
    path('crud-delete/<slug:model>/<slug:id>/', CrudDeleteView.as_view(), name='crud_delete'),
    path('crud-update/<slug:model>/<slug:id>/', CrudUpdateView.as_view(), name='crud_update'),
]

app_name = 'database'
