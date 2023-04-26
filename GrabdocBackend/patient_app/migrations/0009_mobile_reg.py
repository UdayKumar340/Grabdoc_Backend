# Generated by Django 4.1.6 on 2023-04-25 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0008_delete_mobile_reg'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile_Reg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('device_id', models.CharField(max_length=100)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('otp', models.PositiveIntegerField(unique=True)),
            ],
        ),
    ]
