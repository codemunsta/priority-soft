from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from users.custom_authentication import CustomAuthentication
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Inventory Management System",
        default_version="1.0.1",
        description="Documentation for Inventory Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="click2bundi@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny,],
    authentication_classes=[TokenAuthentication, CustomAuthentication]
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('users/', include("users.urls")),
    path('store/', include("store.urls"))
]

urlpatterns += staticfiles_urlpatterns()
