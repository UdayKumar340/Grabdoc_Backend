# Generated by Django 4.1.6 on 2023-05-26 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0016_patientschedulemedicalrecord'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='patientschedulemedicalrecord',
            unique_together={('patient_schedule', 'medical_record')},
        ),
    ]