# Generated by Django 3.2.8 on 2021-10-27 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=128, unique=True, verbose_name='семантический url'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=128, unique=True, verbose_name='заголовок тэга'),
        ),
    ]
