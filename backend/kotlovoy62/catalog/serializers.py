from django.core.exceptions import ObjectDoesNotExist
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .custom_utils import file_delete
from .models import (Element, ElementHasGroup, ElementHasProductPhoto, Group,
                     ProductPhoto, Вrand)


class ВrandSerializer(serializers.ModelSerializer):
    display_order = serializers.IntegerField(
        max_value=32767, min_value=0, default=999,
    )
    image = Base64ImageField()

    def update(self, instance, validated_data):
        new_title = validated_data.get('title', instance.title)
        new_image = validated_data.get('image')
        if new_image:
            file_delete(instance.image)

        instance.title = new_title
        instance.image = validated_data.get('image', instance.image)
        instance.display_order = validated_data.get(
            'display_order', instance.display_order
        )
        instance.save()

        return instance

    class Meta:
        model = Вrand
        fields = ('id', 'title', 'image', 'display_order',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title',)


class ProductPhotoSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    display_order = serializers.IntegerField(
        max_value=32767, min_value=0, default=999,
    )

    class Meta:
        model = ProductPhoto
        fields = ('id', 'image', 'display_order',)


class ElementSerializer(serializers.ModelSerializer):
    images = ProductPhotoSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    brand = ВrandSerializer(read_only=True)
    article = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=Element.objects.all())]
    )
    cur_price = serializers.SerializerMethodField()

    class Meta:
        model = Element
        fields = (
            'id', 'title', 'measurement_unit', 'description', 'images',
            'price', 'stock', 'article', 'available', 'created', 'created',
            'brand', 'groups', 'cur_price',
        )

    def get_cur_price(self, obj):
        req_user = self.context.get('request').user
        if req_user.is_anonymous:
            return obj.price
        price = obj.price - round(obj.price * req_user.discount / 100)
        return price

    def create(self, validated_data):
        images = validated_data.pop('images')
        validated_images = []
        if images['images']:
            for image in images['images']:
                try:
                    img_obj = ProductPhoto.objects.get(pk=image['id'])
                    validated_images.append(img_obj)
                except BaseException:
                    raise serializers.ValidationError(
                        {
                            'images': [
                                f'Передан не правильный параметр: {image}'
                            ]
                        }
                    )

        groups = validated_data.pop('groups')
        validated_groups = []
        if groups['groups']:
            for group in groups['groups']:
                try:
                    group_obj = Group.objects.get(pk=group['id'])
                    validated_groups.append(group_obj)
                except BaseException:
                    raise serializers.ValidationError(
                        {
                            'groups': [
                                f'Передан не правильный параметр: {group}'
                            ]
                        }
                    )

        brand_id = validated_data.pop('brand')
        if brand_id['brand']:
            try:
                brand_id = brand_id['brand']['id']
                brand = Вrand.objects.get(pk=brand_id)
            except BaseException:
                raise serializers.ValidationError(
                    {
                        'brand': [
                            "Передан не правильный параметр: "
                            f"{brand_id['brand']}"
                        ]
                    }
                )
        else:
            brand = None

        element = Element.objects.create(**validated_data)

        for image in validated_images:
            ElementHasProductPhoto.objects.create(
                element=element, photo=image
            )
        for group in validated_groups:
            ElementHasGroup.objects.create(element=element, group=group)
        element.brand = brand

        return element

    def update(self, instance, validated_data):
        images = validated_data.pop('images')
        validated_images = []
        if images['images']:
            for image in images['images']:
                try:
                    img_obj = ProductPhoto.objects.get(pk=image['id'])
                    validated_images.append(img_obj)
                except BaseException:
                    raise serializers.ValidationError(
                        {
                            'images': [
                                f'Передан не правильный параметр: {image}'
                            ]
                        }
                    )

        groups = validated_data.pop('groups')
        validated_groups = []
        if groups['groups']:
            for group in groups['groups']:
                try:
                    group_obj = Group.objects.get(pk=group['id'])
                    validated_groups.append(group_obj)
                except BaseException:
                    raise serializers.ValidationError(
                        {
                            'groups': [
                                f'Передан не правильный параметр: {group}'
                            ]
                        }
                    )

        brand_id = validated_data.pop('brand')
        if brand_id['brand']:
            try:
                brand_id = brand_id['brand']['id']
                brand = Вrand.objects.get(pk=brand_id)
            except Вrand.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        'brand': [
                            "Передан не правильный параметр: "
                            f"{brand_id['brand']}"
                        ]
                    }
                )
        else:
            brand = None

        element = Element.objects.filter(pk=instance.id)
        instance = validated_data.pop('instance')
        element.update(**validated_data)

        old_images = [item[0] for item in instance.images.values_list('id')]
        old_groups = [item[0] for item in instance.groups.values_list('id')]

        for image in validated_images:
            if image.id in old_images:
                old_images.remove(image.id)
            else:
                ElementHasProductPhoto.objects.get_or_create(
                    element=instance, photo=image
                )
        for image_id in old_images:
            del_elem_img = ElementHasProductPhoto.objects.filter(
                element=instance.id, photo=image_id
            )
            try:
                del_image = ProductPhoto.objects.get(pk=image_id)
            except ObjectDoesNotExist as err:
                print(
                    f'В БД запись таблицы "ProductPhoto" с pk={image_id} '
                    'не обнаружена, в процессе выполнения кода возникло '
                    f'исключение: {err}'
                )
            else:
                del_file = del_image.image
                del_image.delete()
                file_delete(del_file)
            finally:
                del_elem_img.delete()

        for group in validated_groups:
            if group.id in old_groups:
                old_groups.remove(group.id)
            else:
                ElementHasGroup.objects.get_or_create(
                    element=instance, group=group
                )
        for group_id in old_groups:
            del_elem_group = ElementHasGroup.objects.filter(
                element=instance.id, group=group_id
            )
            del_elem_group.delete()

        if brand:
            element.update(brand=brand)
        else:
            element.update(brand=None)

        instance.refresh_from_db()
        return instance
