# Generated by Django 3.2.15 on 2022-08-29 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20220826_1939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='inStock',
            new_name='in_stock',
        ),
    ]
