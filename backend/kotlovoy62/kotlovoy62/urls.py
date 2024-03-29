from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi  # delete after development
from drf_yasg.views import get_schema_view  # delete after development
from rest_framework import permissions

# delete after development
schema_view = get_schema_view(
   openapi.Info(
      title="Kotlovoy62 API",
      default_version='v1',
      description="Документация для Kotlovoy62",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
#


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('users.urls')),
    path('api/', include('catalog.urls')),
    path('api/', include('swiper.urls')),
    path('api/', include('orders.urls')),
]

admin.site.site_header = 'Админка Kotlovoy62.ru'
admin.site.site_title = 'Админка'
admin.site.index_title = 'Добро пожаловать в интерфейс администратора!'

# delete after development
urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
]
#

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
