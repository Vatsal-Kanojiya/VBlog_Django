# Generated by Django 4.2.3 on 2023-10-05 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_smarttransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='smarttransaction',
            name='status',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='smarttransaction',
            name='idc',
            field=models.CharField(blank=True, default='ooo', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='smarttransaction',
            name='idu',
            field=models.CharField(max_length=10),
        ),
    ]
