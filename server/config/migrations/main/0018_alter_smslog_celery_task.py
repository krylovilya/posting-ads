# Generated by Django 3.2.9 on 2021-11-25 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20211124_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smslog',
            name='celery_task',
            field=models.CharField(max_length=36, verbose_name='номер celery задачи'),
        ),
    ]