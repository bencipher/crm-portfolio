# Generated by Django 4.0.3 on 2022-03-23 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gateway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jwt',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
