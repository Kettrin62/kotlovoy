from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ElementViewSet, GroupViewSet, ProductPhotosViewSet,
                    ВrandViewSet, say_to_us__view)

router_v1 = DefaultRouter()
router_v1.register('brands', ВrandViewSet, basename='brands')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('elements', ElementViewSet, basename='elements')
router_v1.register(
    'product_photos', ProductPhotosViewSet, basename='product_photos'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/say_to_us/', say_to_us__view, name='say_to_us'),
]
