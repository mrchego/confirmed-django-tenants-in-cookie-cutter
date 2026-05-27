from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from strawberry.django.views import GraphQLView

from config.schema import schema

urlpatterns = [
    # Tenant debug endpoint
    path("", include("config.urls_public")),
    
    # GraphQL endpoint with GraphiQL interface for testing
    path(
        "graphql/",
        GraphQLView.as_view(schema=schema, graphiql=True),
        name="graphql",
    ),
    
    # Admin
    path(settings.ADMIN_URL, admin.site.urls),
    
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]