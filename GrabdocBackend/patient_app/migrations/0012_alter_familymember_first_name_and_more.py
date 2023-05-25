# Generated by Django 4.1.6 on 2023-05-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0011_familymember_delete_addnewpatient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='familymember',
            unique_together={('patient', 'first_name', 'last_name')},
        ),
    ]
