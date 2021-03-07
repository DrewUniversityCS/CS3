from django.urls import path

from database.views import CrudView, CrudDeleteView

urlpatterns = [
    path('crud/<slug:model>/', CrudView.as_view(), name='crud_model'),
    path('crud-delete/<slug:model>/<slug:id>/', CrudDeleteView.as_view(), name='crud_delete'),
]

app_name = 'database'
