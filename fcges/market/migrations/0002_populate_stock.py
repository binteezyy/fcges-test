from __future__ import unicode_literals
from django.db import migrations
from ..models import Stock


def populate_stock(apps, schema_editor):
    stocks = [
        {'name': 'Jolibee', 'code': 'JFC', 'price': '10.0'},
        {'name': 'Globe', 'code': 'GLO', 'price' : '5.2'},
        {'name': 'DITO', 'code': 'DITO', 'price': '9.8'}
    ]

    for stock in stocks:
        Stock.objects.get_or_create(**stock)

class Migration(migrations.Migration):
    dependencies = [
        ('market', '0001_initial')
    ]

    operations = [
        migrations.RunPython(populate_stock),
    ]