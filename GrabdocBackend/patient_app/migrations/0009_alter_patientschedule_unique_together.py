# Generated by Django 4.1.6 on 2023-05-23 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0008_patientschedule'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='patientschedule',
            unique_together={('doctors_schedule', 'patient')},
        ),
    ]