# Generated by Django 2.1 on 2018-10-30 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_remove_business_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]