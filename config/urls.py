from django.conf import settings
from django.urls import include, path
import debug_toolbar
from django.conf.urls.static import static
from confirming_django_tenants.core.views import tenant_debug
from django.contrib import admin

urlpatterns = [
    path("", tenant_debug),
    path(settings.ADMIN_URL, admin.site.urls),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] 
        
        
