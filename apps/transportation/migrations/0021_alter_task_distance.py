# Generated by Django 5.1.6 on 2025-03-02 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0020_alter_notification_notification_importance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='distance',
            field=models.FloatField(default=0),
        ),
    ]
