# Generated by Django 5.1.6 on 2025-02-24 12:42

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0005_alter_car_car_insurance_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='birthday_date',
            field=django_jalali.db.models.jDateField(),
        ),
        migrations.AlterField(
            model_name='driver',
            name='sertificate_expiration_date',
            field=django_jalali.db.models.jDateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=django_jalali.db.models.jDateField(),
        ),
    ]
