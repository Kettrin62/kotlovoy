from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'v1/users/password_reset/',
        include('django_rest_passwordreset.urls', namespace='password_reset')
    ),
    path('v1/', include(router_v1.urls)),
]
