# Generated by Django 4.1.6 on 2024-01-31 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorSpecialities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality_name', models.CharField(blank=True, max_length=200, null=True)),
                ('speciality_description', models.CharField(blank=True, max_length=400, null=True)),
            ],
            options={
                'db_table': 'doctor_specialities',
            },
        ),
        migrations.CreateModel(
            name='DoctorTimeSlots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.DateTimeField(null=True)),
                ('repeat', models.CharField(choices=[('Does not Repeat', 'Does not Repeat'), ('Daily', 'Daily'), ('Weekly on Monday', 'Weekly on Moanday'), ('Every Week (Monday to Friday)', 'Every Week (Monday to Friday)'), ('Monthly on the First Monday', 'Monthly on the First Monday'), ('Yearly', 'Yearly'), ('Coustom', 'Coustom')], default='Does not Repeat', max_length=100)),
            ],
            options={
                'db_table': 'doctor_time_slots',
            },
        ),
    ]
