# Generated by Django 4.1.5 on 2023-05-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttransactions',
            name='satisfied',
            field=models.BooleanField(default=False),
        ),
    ]