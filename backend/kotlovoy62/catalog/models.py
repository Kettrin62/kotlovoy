import os
from hashlib import sha1

from django.db import models

UPLOAD_ROOT_DIR = {
    'Вrand': 'brands',
    'ProductPhoto': 'elements'
}


def get_image_path(instance, filename):
    parse_name = str.encode(filename)
    parse_type = str(filename).split('.')[-1]
    hash_name = sha1(parse_name).hexdigest() + '.' + parse_type
    root_dir = UPLOAD_ROOT_DIR.get(instance.__class__.__name__)
    return os.path.join(root_dir, hash_name[:2], hash_name[2:4], hash_name)


class Вrand(models.Model):
    title = models.CharField(
        verbose_name='Название бренда',
        max_length=100,
        unique=True
    )
    image = models.ImageField(
        upload_to=get_image_path,
        blank=True, null=True,
        verbose_name='Картинка',
    )
    display_order = models.PositiveSmallIntegerField(
        verbose_name='Порядок отображения',
    )

    class Meta:
        ordering = ('display_order', 'title')
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        constraints = (
            models.UniqueConstraint(
                fields=['title'],
                name='unique brand value'
            ),
        )

    def __str__(self):
        return '{}'.format(self.title,)


class Group(models.Model):
    title = models.CharField(
        verbose_name='Название группы/модели',
        max_length=150,
        unique=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Модель/Группа'
        verbose_name_plural = 'Модели/Группы'
        constraints = (
            models.UniqueConstraint(
                fields=['title'],
                name='unique group value'
            ),
        )

    def __str__(self):
        return '{}'.format(self.title,)


class ProductPhoto(models.Model):
    image = models.ImageField(
        upload_to=get_image_path,
        blank=True, null=True,
        verbose_name='Фото',
    )
    display_order = models.PositiveSmallIntegerField(
        verbose_name='Порядок отображения',
    )

    class Meta:
        ordering = ('display_order',)
        verbose_name = 'Фото продукции'
        verbose_name_plural = 'Фото продукции'

    def __str__(self):
        return 'Фото {}'.format(self.image)


class Element(models.Model):
    title = models.CharField(
        verbose_name='Название детали',
        max_length=200,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name='Ед. измерения',
        max_length=30,
        default='шт.'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    images = models.ManyToManyField(
        ProductPhoto,
        through='ElementHasProductPhoto',
        related_name='photos',
        verbose_name='Фото',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    stock = models.PositiveIntegerField(
        verbose_name='Кол-во в наличии',
    )
    article = models.CharField(
        verbose_name='Артикул',
        max_length=50,
        db_index=True,
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Отображение на сайте',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования',
    )
    brand = models.ForeignKey(
        Вrand,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='elements',
        verbose_name='Производитель',
    )
    groups = models.ManyToManyField(
        Group,
        through='ElementHasGroup',
        related_name='groups',
        verbose_name='Модели/Группы',
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'article'],
                name='unique element value'
            ),
        )

    def __str__(self):
        return '{}'.format(self.title)


class ElementHasGroup(models.Model):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        verbose_name='Деталь'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Модель/Группа',
        related_name='groups_has_elm',
    )

    class Meta:
        verbose_name = 'Пункт'
        verbose_name_plural = 'Принадлежность к группам'
        constraints = (
            models.UniqueConstraint(
                fields=['element', 'group'],
                name='unique elements in group value'
            ),
        )

    def __str__(self):
        return 'В группе "{}"'.format(self.group)


class ElementHasProductPhoto(models.Model):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        verbose_name='Деталь'
    )
    photo = models.ForeignKey(
        ProductPhoto,
        on_delete=models.CASCADE,
        verbose_name='Фото детали'
    )

    class Meta:
        verbose_name = 'Снимок детали'
        verbose_name_plural = 'Снимки деталей'

    def __str__(self):
        return '{} {}'.format(self.photo, self.element)
