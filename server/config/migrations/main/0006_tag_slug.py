# Generated by Django 3.2.8 on 2021-10-27 13:33

import apps.main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20211025_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='', max_length=128, verbose_name='семантический url'),
        ),
    ]