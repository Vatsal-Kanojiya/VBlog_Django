# Generated by Django 4.1.10 on 2023-10-23 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0009_smarttransaction_transaction_st_tm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smarttransaction',
            old_name='transaction_st_tm',
            new_name='transaction_dt_tm',
        ),
    ]
