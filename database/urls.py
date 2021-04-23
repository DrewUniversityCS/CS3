from django.urls import path

from database.pseudo_views import load_dropdown_options
from database.views import CrudView, CrudDeleteView, CrudUpdateView, CrudInspectView, DynamicModelSetCreateView, \
    DynamicModelSetUpdateView, DynamicModelSetInspectView, DynamicModelSetDeleteView, CreateBulkSectionsView, \
    CreateBulkSectionsSuccessView, CreatePreferenceView

urlpatterns = [
    path('crud/<slug:model>/', CrudView.as_view(), name='crud_model'),
    path('crud-inspect/<slug:model>/<slug:id>/', CrudInspectView.as_view(), name='crud_inspect'),
    path('crud-delete/<slug:model>/<slug:id>/', CrudDeleteView.as_view(), name='crud_delete'),
    path('crud-update/<slug:model>/<slug:id>/', CrudUpdateView.as_view(), name='crud_update'),

    path('crud/create-bulk-sections', CreateBulkSectionsView.as_view(), name='sections_bulk'),
    path('crud/create-bulk-sections/success', CreateBulkSectionsSuccessView.as_view(), name='sections_bulk_success'),
    path('crud/create-preference', CreatePreferenceView.as_view(), name='create_preference'),

    path('set-crud/<slug:model>/', DynamicModelSetCreateView.as_view(), name='set_crud'),
    path('set-inspect/<slug:model>/<slug:id>/', DynamicModelSetInspectView.as_view(), name='set_crud_inspect'),
    path('set-delete/<slug:model>/<slug:id>/', DynamicModelSetDeleteView.as_view(), name='set_crud_delete'),
    path('set-update/<slug:model>/<slug:id>/', DynamicModelSetUpdateView.as_view(), name='set_crud_update'),
       
    # AJAX views
    path('ajax/load-dropdown-options/', load_dropdown_options, name='ajax_load_dropdown_options')
]

app_name = 'database'
