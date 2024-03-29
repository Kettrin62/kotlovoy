from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny

from kotlovoy62.settings import (
    CUSTOM_SETTINGS_DRF, DEFAULT_FROM_EMAIL, FEEDBACK_BOX
)

from .custom_utils import file_delete
from .models import (
    Element, ElementHasProductPhoto, Group, ProductPhoto, Вrand
)
from .permissions import IsAdminOrReadOnly
from .serializers import (ElementSerializer, GroupSerializer,
                          ProductPhotoSerializer, ВrandSerializer)


class ВrandViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    queryset = Вrand.objects.all()
    serializer_class = ВrandSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        file_delete(instance.image)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete',)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(
        ['get'], detail=True,
        permission_classes=(IsAdminOrReadOnly,)
    )
    def related_to_brand(self, request, pk):
        arr = Group.objects.filter(
            groups_has_elm__element__brand_id=pk
        ).distinct()
        serializer = GroupSerializer(arr, many=True)
        return Response(serializer.data)


class ProductPhotosViewSet(viewsets.ModelViewSet):
    http_method_names = ('post', 'delete',)
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        file_delete(instance.image)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = CUSTOM_SETTINGS_DRF.get('PAGE_SIZE_ELEMENTS')


class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('brand', 'groups')
    search_fields = ('title', 'article',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = RecipeSetPagination

    def perform_create(self, serializer):
        try:
            serializer.save(
                brand={'brand': (self.request.data['brand'])},
                images={'images': (self.request.data['images'])},
                groups={'groups': (self.request.data['groups'])},
            )
        except KeyError as err:
            raise ValidationError(
                {
                    'message': [
                        'В запросе не передан параметр: {}'.format(err)
                    ]
                }
            )

    def perform_update(self, serializer):
        element = self.get_object()
        try:
            serializer.save(
                instance=element,
                brand={'brand': (self.request.data['brand'])},
                images={'images': (self.request.data['images'])},
                groups={'groups': (self.request.data['groups'])},
            )
        except KeyError as err:
            raise ValidationError(
                {
                    'message': [
                        'В запросе не передан параметр: {}'.format(err)
                    ]
                }
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        images = ElementHasProductPhoto.objects.filter(element=instance)
        for item in images:
            file = item.photo.image
            self.perform_destroy(item.photo)
            file_delete(file)

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def say_to_us__view(request):
    name = request.data.get('name')
    feedback = request.data.get('feedback')
    msg_text = request.data.get('text')
    if not (name and feedback and msg_text):
        raise ValidationError(
                {'message': ['Все поля обязательны к заполнению!']}
            )

    title = (f'У вас новое сообщение от {name} с сайта Kotlovoy62.ru')
    message = (
        f'Текст обращения:\n{msg_text}\n\nДля связи {name} указал(а): '
        f'{feedback}'
    )
    send_mail(title, message, DEFAULT_FROM_EMAIL, [FEEDBACK_BOX])
    return Response(
        data={'message': ['Сообщение успешно отправлено на почту']},
        status=status.HTTP_200_OK
    )
