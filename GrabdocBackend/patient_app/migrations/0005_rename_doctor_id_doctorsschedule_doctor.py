# Generated by Django 4.1.6 on 2023-05-18 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0004_doctorsschedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorsschedule',
            old_name='doctor_id',
            new_name='doctor',
        ),
    ]
