from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from kotlovoy62.settings import CUSTOM_SETTINGS_DRF

from .models import User
from .permissions import (IsAdminOrUserHimself,
                          IsAdminOrUserHimselfAndNotSafeMethods, IsUserHimself)
from .serializers import (SetPasswordSerializer, UserCreateSerializer,
                          UserSerializer)


class UserSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = CUSTOM_SETTINGS_DRF.get('PAGE_SIZE_USERS')


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'username', 'phoneNumber')
    pagination_class = UserSetPagination
    permission_classes = (IsAdminOrUserHimselfAndNotSafeMethods,)

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        else:
            return UserSerializer

    @action(
        ['get'], detail=False,
        permission_classes=(IsAdminOrUserHimself,)
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        ['post'], detail=False,
        permission_classes=(IsUserHimself,)
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
