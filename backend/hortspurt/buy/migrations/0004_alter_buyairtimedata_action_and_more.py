# Generated by Django 5.0.1 on 2024-06-22 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy', '0003_alter_buyairtimedata_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyairtimedata',
            name='action',
            field=models.CharField(choices=[('Received', 'Received'), ('Self', 'Self'), ('Gift', 'Gift')], max_length=8),
        ),
        migrations.AlterField(
            model_name='buyairtimedata',
            name='service',
            field=models.CharField(choices=[('Data', 'Data'), ('Airtime', 'Airtime')], max_length=8),
        ),
    ]
