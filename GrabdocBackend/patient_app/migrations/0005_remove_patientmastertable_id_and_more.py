# Generated by Django 4.1.6 on 2023-02-02 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0004_alter_patientmastertable_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientmastertable',
            name='id',
        ),
        migrations.AlterField(
            model_name='patientmastertable',
            name='patient_id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
