# Generated by Django 2.1 on 2018-11-01 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20181101_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sans',
            name='end_time',
            field=models.CharField(default='00:00', max_length=5),
        ),
        migrations.AlterField(
            model_name='sans',
            name='start_time',
            field=models.CharField(default='00:00', max_length=5),
        ),
    ]