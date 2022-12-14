# Generated by Django 3.2.15 on 2022-08-22 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_auto_20220822_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='score',
            field=models.PositiveSmallIntegerField(choices=[(5, 'excellent'), (4, 'very good'), (3, 'good'), (2, 'poor'), (1, 'bad')], default=0),
        ),
    ]
