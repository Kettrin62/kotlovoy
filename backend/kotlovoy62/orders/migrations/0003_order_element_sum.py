# Generated by Django 4.0.5 on 2022-10-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='element_sum',
            field=models.PositiveIntegerField(default=0, verbose_name='Стоимость товаров'),
        ),
    ]
