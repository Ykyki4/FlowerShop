# Generated by Django 4.1.5 on 2023-01-22 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_consultationsummary'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Статистика заказа',
                'verbose_name_plural': 'Статистика заказов',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('backend.order',),
        ),
    ]
