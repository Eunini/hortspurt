# Generated by Django 5.0.1 on 2024-06-22 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_alter_addmoneytransaction_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addmoneytransaction',
            name='method',
            field=models.CharField(choices=[('USSD', 'USSD'), ('Bank Transfer', 'Bank Transfer')], default='U', max_length=15),
        ),
    ]
