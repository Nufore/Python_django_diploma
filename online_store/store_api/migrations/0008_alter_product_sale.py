# Generated by Django 4.2.2 on 2023-08-13 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_api', '0007_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store_api.sale'),
        ),
    ]