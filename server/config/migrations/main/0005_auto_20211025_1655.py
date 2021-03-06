# Generated by Django 3.2.8 on 2021-10-25 09:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20211024_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='дата изменения'),
        ),
        migrations.AddField(
            model_name='tag',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 10, 25, 9, 55, 0, 602006, tzinfo=utc), verbose_name='дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='дата изменения'),
        ),
    ]
