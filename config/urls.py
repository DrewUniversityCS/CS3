from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from dataingest import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('upload/', views.upload, name='upload'),
    path('csv/', views.csv_list, name='csv_list'),
    path('csv/upload', views.upload_csv, name='upload_csv'),
    path('', include('pages.urls', namespace='pages')),
    path('', include('database.urls', namespace='database')),
    path('', include('dataingest.urls', namespace='dataingest')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
