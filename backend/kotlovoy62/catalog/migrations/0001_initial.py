# Generated by Django 4.0.5 on 2022-09-16 07:43

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Название детали')),
                ('measurement_unit', models.CharField(default='шт.', max_length=30, verbose_name='Ед. измерения')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('stock', models.PositiveIntegerField(verbose_name='Кол-во в наличии')),
                ('article', models.CharField(db_index=True, max_length=50, verbose_name='Артикул')),
                ('available', models.BooleanField(default=True, verbose_name='Отображение на сайте')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
            ],
            options={
                'verbose_name': 'Деталь',
                'verbose_name_plural': 'Детали',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='ElementHasGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Пункт',
                'verbose_name_plural': 'Принадлежность к группам',
            },
        ),
        migrations.CreateModel(
            name='ElementHasProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Снимок детали',
                'verbose_name_plural': 'Снимки деталей',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Модель/Группа')),
            ],
            options={
                'verbose_name': 'Модель/Группа',
                'verbose_name_plural': 'Модели/Группы',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=catalog.models.get_image_path, verbose_name='Фото')),
                ('display_order', models.PositiveSmallIntegerField(verbose_name='Порядок отображения')),
            ],
            options={
                'verbose_name': 'Фото продукции',
                'verbose_name_plural': 'Фото продукции',
                'ordering': ('display_order',),
            },
        ),
        migrations.CreateModel(
            name='Вrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Бренд')),
                ('image', models.ImageField(blank=True, null=True, upload_to=catalog.models.get_image_path, verbose_name='Картинка')),
                ('display_order', models.PositiveSmallIntegerField(verbose_name='Порядок отображения')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ('display_order', 'title'),
            },
        ),
        migrations.AddConstraint(
            model_name='вrand',
            constraint=models.UniqueConstraint(fields=('title',), name='unique brand value'),
        ),
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('title',), name='unique group value'),
        ),
        migrations.AddField(
            model_name='elementhasproductphoto',
            name='element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.element', verbose_name='Деталь'),
        ),
        migrations.AddField(
            model_name='elementhasproductphoto',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productphoto', verbose_name='Фото детали'),
        ),
        migrations.AddField(
            model_name='elementhasgroup',
            name='element',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.element', verbose_name='Деталь'),
        ),
        migrations.AddField(
            model_name='elementhasgroup',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.group', verbose_name='Модель/Группа'),
        ),
        migrations.AddField(
            model_name='element',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='catalog.вrand', verbose_name='Производитель'),
        ),
        migrations.AddField(
            model_name='element',
            name='groups',
            field=models.ManyToManyField(related_name='groups', through='catalog.ElementHasGroup', to='catalog.group', verbose_name='Модели/Группы'),
        ),
        migrations.AddField(
            model_name='element',
            name='images',
            field=models.ManyToManyField(related_name='photos', through='catalog.ElementHasProductPhoto', to='catalog.productphoto', verbose_name='Фото'),
        ),
        migrations.AddConstraint(
            model_name='elementhasgroup',
            constraint=models.UniqueConstraint(fields=('element', 'group'), name='unique elements in group value'),
        ),
        migrations.AddConstraint(
            model_name='element',
            constraint=models.UniqueConstraint(fields=('title', 'article'), name='unique element value'),
        ),
    ]
