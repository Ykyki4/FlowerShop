# Generated by Django 4.1.5 on 2023-01-22 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_order_yookassa_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='consultation',
        ),
        migrations.AddField(
            model_name='consultation',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='backend.order', verbose_name='Заказ'),
        ),
    ]
