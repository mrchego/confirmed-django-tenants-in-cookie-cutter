from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

import debug_toolbar

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="pages/home.html"),
        name="home",
    ),

    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]