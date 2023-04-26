# Generated by Django 4.1.6 on 2023-04-25 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0006_consultantdiseasetable_specalitymastertable_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile_Reg',
            fields=[
                ('PhoneNumber', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('patient_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('otp', models.PositiveIntegerField(max_length=6, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlottable',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('start_time', models.TimeField(verbose_name='Show start time')),
                ('duration', models.DurationField(verbose_name='Duration od time')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='end time')),
            ],
            options={
                'db_table': 'doctors_time_slots_table',
            },
        ),
        migrations.AlterField(
            model_name='patientmastertable',
            name='patient_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
