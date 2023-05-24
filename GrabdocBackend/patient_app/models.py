from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 

#class PatientmasterManager(models.Manager):
#   def create(self, *args, **kwargs):
#      print("manager calling..")
#     max_patient_id = PatientMasterTable.objects.latest('patient_id')
#    print("max patient id", max_patient_id)
#    kwargs['patient_id'] =int(max_patient_id)+1 if max_patient_id else 100000
#    super(PatientmasterManager, self).create(*args, **kwargs)


class Mobile_Reg(models.Model):
    phone_number = models.CharField(max_length=10, null= False, blank=False)
    device_id = models.CharField(max_length=100)
    is_phone_verified = models.BooleanField(default = False)
    ctime = models.DateTimeField(auto_now_add=True, blank=True)
    otp = models.PositiveIntegerField(null = True)
    number_of_attements = models.IntegerField(default=0)


class PatientMasterTable(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    patient_first_name = models.CharField(max_length= 200, null=True, blank = True)
    patient_last_name = models.CharField(max_length= 200, null=True, blank = True)
    gendar = models.CharField(max_length= 200, null=True, blank = True)
    email = models.CharField(max_length= 200, null=True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    username = models.CharField(('Phone Number'), validators=[phone_regex], max_length=17, unique=True)
    height = models.IntegerField(null = True, blank = True)
    weight = models.IntegerField(null = True, blank = True)
    blood_group = models.CharField(max_length=10,null = True, blank = True)

    

    USERNAME_FIELD = 'username'
#    objects = PatientmasterManager()
#   def __str__(self):
#        return (self.patient_first_name,self.patient_last_name)



class ConsultantDiseaseTable(models.Model):
    disease_type = models.CharField(max_length = 300, null = True, blank = True)

    class Meta:
        db_table= 'consultant_disease_table'

class SpecalityMastertable(models.Model):

    specality_name = models.CharField(max_length = 200, null = True, blank = True)
    specality_description = models.CharField(max_length = 400, null = True, blank = True)

    class Meta:
        db_table = 'specality_master_table'


class Doctors(models.Model):
    name = models.CharField(max_length= 200, null=True, blank = True)
    specality =  models.ForeignKey(SpecalityMastertable, on_delete=models.CASCADE)
    experience = models.IntegerField(null = True, blank = True)
    online = models.BooleanField()
    language = models.CharField(max_length= 200, null=True, blank = True)
    location = models.CharField(max_length= 200, null=True, blank = True)
    about_doctor = models.TextField(null=True, blank = True)



class DoctorsSchedule(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    time_slot = models.DateTimeField(null=True)


class PatientSummary(models.Model):
    summary = models.TextField(null=True, blank = True)
    patient = models.OneToOneField(PatientMasterTable, on_delete=models.CASCADE,primary_key=True)

class PatientSchedule(models.Model):
    doctors_schedule = models.ForeignKey(DoctorsSchedule, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientMasterTable, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctors_schedule', 'patient',)


