# Generated by Django 4.0.5 on 2022-08-26 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_group_title_group_unique group value'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Фото продукции',
                'verbose_name_plural': 'Фото продукции',
            },
        ),
        migrations.CreateModel(
            name='ElementHasProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.element', verbose_name='Деталь')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productphoto', verbose_name='Фото детали')),
            ],
            options={
                'verbose_name': 'Фото детали',
                'verbose_name_plural': 'Фото детали',
            },
        ),
    ]
