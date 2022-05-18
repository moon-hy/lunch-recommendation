import django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
 
schema_url_v1_patterns = [
    path(r'^api/auth/', include('authentication.urls')),
    path(r'^api/community/', include('community.urls')),
    path(r'^api/feature/', include('feature.urls')),
    path(r'^api/account/', include('account.urls')),
    path(r'^api/recommendation/', include('recommendation.urls')),
]
 
schema_view_v1 = get_schema_view(
    openapi.Info(
        title="NYOM Open API",
        default_version='v1',
        description="NYOM Open API Docs",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="License"),
    ),
    validators=['flex'], #'ssv'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)
 

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', )
    path('api/auth/', include('authentication.urls')),
    path('api/community/', include('community.urls')),
    path('api/feature/', include('feature.urls')),
    path('api/account/', include('account.urls')),
    path('api/recommendation/', include('recommendation.urls')),

    # Auto DRF API docs
    # path(r'swagger(?P<format>\.json|\.yaml)', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
