# Generated by Django 5.0.4 on 2024-05-06 20:15

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 6, 20, 15, 52, 165561)),
        ),
        migrations.AlterField(
            model_name='otp',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
