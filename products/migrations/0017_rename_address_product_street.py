# Generated by Django 3.2.15 on 2022-09-09 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20220909_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='address',
            new_name='street',
        ),
    ]