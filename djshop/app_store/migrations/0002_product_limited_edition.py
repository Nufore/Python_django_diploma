# Generated by Django 4.1.5 on 2023-05-11 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='limited_edition',
            field=models.BooleanField(default=False, null=True),
        ),
    ]