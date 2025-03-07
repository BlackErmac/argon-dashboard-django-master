# Generated by Django 5.1.6 on 2025-03-06 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0025_car_fuel_mount'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='transportation.car'),
        ),
        migrations.AddField(
            model_name='notification',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='transportation.driver'),
        ),
        migrations.AddField(
            model_name='notification',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='transportation.task'),
        ),
    ]
