# Generated by Django 4.2.3 on 2024-07-04 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_dollaraccount_dollar_rate'),
        ('core', '0015_recipient_account_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recipient',
            unique_together={('kyc', 'account_type')},
        ),
    ]
