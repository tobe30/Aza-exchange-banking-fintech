# Generated by Django 4.2.3 on 2024-06-28 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_transaction_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='currency',
            field=models.CharField(choices=[('NGN', 'Naira'), ('USD', 'Dollar')], default='NGN', max_length=10),
        ),
    ]
