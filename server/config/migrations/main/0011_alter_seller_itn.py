# Generated by Django 3.2.9 on 2021-11-07 12:00

import apps.main.services.validate_itn
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20211104_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='itn',
            field=models.CharField(max_length=12, validators=[apps.main.services.validate_itn.validate_itn], verbose_name='идентификационный номер налогоплательщика'),
        ),
    ]
