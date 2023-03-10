# Generated by Django 4.1.5 on 2023-01-19 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_remove_consultation_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='consultation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='consultations', to='backend.consultation', verbose_name='Констультация'),
        ),
    ]
