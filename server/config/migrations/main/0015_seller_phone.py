# Generated by Django 3.2.9 on 2021-11-23 12:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_smslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='phone',
            field=models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(message='Не верный номер телефона.', regex='^\\+?1?\\d{11}$')], verbose_name='номер телефона в формате +7'),
        ),
    ]
