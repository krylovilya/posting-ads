# Generated by Django 3.2.8 on 2021-10-24 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_ad_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='name',
            field=models.CharField(default='test', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default='test', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default='test', max_length=128),
            preserve_default=False,
        ),
    ]
