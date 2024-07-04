# Generated by Django 4.2.3 on 2024-06-28 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_recipient_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipients', to=settings.AUTH_USER_MODEL),
        ),
    ]