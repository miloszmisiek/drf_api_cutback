# Generated by Django 3.2.15 on 2022-09-17 19:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_productimage_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='productimage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='../default_gkffon', upload_to='images/'),
        ),
    ]
