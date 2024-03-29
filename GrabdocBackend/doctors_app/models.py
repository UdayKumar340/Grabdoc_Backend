from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 
from django.conf import settings



class ConsultantDiseases(models.Model):
    disease_type = models.CharField(max_length = 300, null = True, blank = True)
    def __str__(self):
        return self.disease_type

    class Meta:
        db_table= 'consultant_diseases'



class DoctorSpecialities(models.Model):

    disease = models.ForeignKey(ConsultantDiseases, on_delete=models.SET_DEFAULT,null=True,default= None)
    speciality_name = models.CharField(max_length = 200, null = True, blank = True)
    speciality_description = models.CharField(max_length = 400, null = True, blank = True)
    def __str__(self):
        return self.speciality_name
   

    class Meta:
        db_table = 'doctor_specialities'


class GrabdocDoctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
    profile_picture = models.CharField(max_length= 50,null=True, blank=True)
    name = models.CharField(max_length= 200, null=True, blank = True)
    designation = models.CharField(max_length= 200, null=True, blank = True)
    email = models.CharField(max_length= 200, null=True, blank = True)
    speciality =  models.ForeignKey(DoctorSpecialities, on_delete=models.CASCADE,null=True,default= None)  
    experience = models.IntegerField(null = True, blank = True,default= None)
    language = models.CharField(max_length= 200, null=True, blank = True)
    location = models.CharField(max_length= 200, null=True, blank = True)
    about_doctor = models.TextField(null=True, blank = True)

    online = models.BooleanField(default=False)
    video_consultation = models.BooleanField(default=True)
    fee = models.CharField(max_length= 20, null=True, blank = True)
    password = models.CharField(max_length= 20, null=True, blank = True)
    default_password = models.BooleanField(default= True)


   
    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'grabdoc_doctor' 
        
    USERNAME_FIELD = 'username'




class DoctorTimeSlots(models.Model):
    doctor = models.ForeignKey(GrabdocDoctor, on_delete=models.CASCADE)
    time_slot = models.DateTimeField(null=True)
    repeat_choices =(
        ('Does not Repeat','Does not Repeat'),
        ('Daily','Daily'),
        ('Weekly on Monday','Weekly on Moanday'),
        ('Every Week (Monday to Friday)','Every Week (Monday to Friday)'),
        ('Monthly on the First Monday','Monthly on the First Monday'),
        ('Yearly','Yearly'),
        ('Coustom','Coustom'),
    )
    repeat = models.CharField(max_length=100,choices=repeat_choices,default= 'Does not Repeat')

    def __str__(self):
        return f'{self.doctor.name} {self.time_slot}'
    class Meta:
        db_table = 'doctor_time_slots'        

