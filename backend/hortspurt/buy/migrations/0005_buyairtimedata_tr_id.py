# Generated by Django 5.0.1 on 2024-06-22 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy', '0004_alter_buyairtimedata_action_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyairtimedata',
            name='tr_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
