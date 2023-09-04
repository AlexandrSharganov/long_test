from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Longevity API",
      default_version='v1',
      description="Документация для приложения long проекта Longevity",
      contact=openapi.Contact(email="admin@example.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
] 
