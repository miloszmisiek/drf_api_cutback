# Generated by Django 3.2.15 on 2022-09-09 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_location_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='product',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='product_location', to='products.product'),
        ),
    ]
