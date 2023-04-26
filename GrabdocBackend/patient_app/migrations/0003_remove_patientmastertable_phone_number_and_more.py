# Generated by Django 4.1.6 on 2023-02-02 14:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0002_alter_patientmastertable_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientmastertable',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='patientmastertable',
            name='username',
            field=models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number'),
        ),
    ]
