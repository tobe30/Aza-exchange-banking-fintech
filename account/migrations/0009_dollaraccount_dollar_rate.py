# Generated by Django 4.2.3 on 2024-06-24 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_dollaraccount_user_alter_kyc_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dollaraccount',
            name='dollar_rate',
            field=models.DecimalField(decimal_places=2, default=1400.0, max_digits=12),
        ),
    ]