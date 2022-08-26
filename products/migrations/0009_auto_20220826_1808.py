# Generated by Django 3.2.15 on 2022-08-26 18:08

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20220826_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=djmoney.models.fields.MoneyField(currency_choices=(('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('PLN', 'PLN')), decimal_places=2, default=Decimal('0'), default_currency='EUR', max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'), ('PLN', 'PLN')], default='EUR', editable=False, max_length=3),
        ),
    ]
