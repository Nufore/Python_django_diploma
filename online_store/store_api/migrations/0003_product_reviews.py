# Generated by Django 4.2.2 on 2023-07-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_api', '0002_rename_avg_rating_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.IntegerField(default=0),
        ),
    ]
