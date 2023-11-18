import os

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

if settings.JSON_WEB_TOKEN_AUTH:
    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView
    )


schema_view = get_schema_view(
   openapi.Info(
      title="Manager API Documentation",
      default_version='v1',
      description="API documentation for the manager.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

admin.site.site_header = os.getenv("XXX_SITE_HEADER", "XXX Feed")
admin.site.site_title = os.getenv("XXX_SITE_TITLE", "XXX Feed Admin")
admin.site.index_title = os.getenv("XXX_SITE_INDEX_TITLE", "Howdy Partner!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('manager.urls', namespace='manager'), name='manager'),
    path('api/', include('api.router', namespace='api'), name='api')
]

if settings.JSON_WEB_TOKEN_AUTH:
    urlpatterns.append(
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    )

if settings.DEBUG:
    urlpatterns.append(
        path(
            'api-docs/', 
            schema_view.with_ui('swagger', cache_timeout=0), 
            name='schema-swagger-ui'
        ),
    )
    urlpatterns +=static(
        settings.STATIC_URL, 
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
