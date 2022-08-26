# Generated by Django 3.2.15 on 2022-08-26 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20220825_1543'),
        ('ratings', '0003_alter_rating_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_rating', to='products.product'),
        ),
    ]
