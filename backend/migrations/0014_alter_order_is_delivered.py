# Generated by Django 4.1.5 on 2023-01-22 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_delivered',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Выполнен'),
        ),
    ]
