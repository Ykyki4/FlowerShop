# Generated by Django 4.1.5 on 2023-01-19 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_order_consultation'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='yookassa_payment_id',
            field=models.CharField(blank=True, max_length=80, verbose_name='ID платежа Юкасса'),
        ),
    ]
