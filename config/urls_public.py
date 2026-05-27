from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from strawberry.django.views import GraphQLView

from config.schema import schema

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="pages/home.html"),
        name="home",
    ),
    
    # GraphQL endpoint for public schema
    path(
        "graphql/",
        GraphQLView.as_view(schema=schema, graphiql=True),
        name="public-graphql",
    ),
    
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]