# Generated by Django 5.0.1 on 2024-06-22 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_addmoneytransaction_tr_ref_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addmoneytransaction',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 22, 13, 42, 8, 554911)),
        ),
        migrations.AddField(
            model_name='addmoneytransaction',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 22, 13, 42, 8, 554911)),
        ),
    ]
