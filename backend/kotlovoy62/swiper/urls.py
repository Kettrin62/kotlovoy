from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SwiperViewSet

router_v1 = DefaultRouter()
router_v1.register('swipers', SwiperViewSet, basename='swipers')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
