from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('pages.urls', namespace='pages')),
    path('', include('database.urls', namespace='database')),
    path('', include('dataingest.urls', namespace='dataingest')),
    path('', include('datacollection.urls', namespace='datacollection')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
