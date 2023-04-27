from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#class PatientmasterManager(models.Manager):
#   def create(self, *args, **kwargs):
#      print("manager calling..")
#     max_patient_id = PatientMasterTable.objects.latest('patient_id')
#    print("max patient id", max_patient_id)
#    kwargs['patient_id'] =int(max_patient_id)+1 if max_patient_id else 100000
#    super(PatientmasterManager, self).create(*args, **kwargs)

# today write the code otp verify
class Mobile_Reg(models.Model):
    phone_number = models.CharField(unique=True,max_length=10, null= True, blank=True)
    device_id = models.CharField(max_length=100)
    is_phone_verified = models.BooleanField(default = False)
    ctime = models.DateTimeField(auto_now_add=True, blank=True)
    otp = models.PositiveIntegerField(unique=True)
    number_of_attements = models.IntegerField(default=0)





class PatientMasterTable(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    patient_id = models.IntegerField(unique=True, primary_key=True)
    patient_first_name = models.CharField(max_length= 200, null=True, blank = True)
    patient_last_name = models.CharField(max_length= 200, null=True, blank = True)
    gendar = models.CharField(max_length= 200, null=True, blank = True)
    email = models.CharField(max_length= 200, null=True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    username = models.CharField(('Phone Number'), validators=[phone_regex], max_length=17, unique=True)
    
    USERNAME_FIELD = 'username'
#    objects = PatientmasterManager()

class ConsultantDiseaseTable(models.Model):
    disease_id  = models.AutoField(unique=True, primary_key = True)
    disease_type = models.CharField(max_length = 300, null = True, blank = True)

    class Meta:
        db_table= 'consultant_disease_table'

class SpecalityMastertable(models.Model):
    specality_id = models.AutoField(unique = True, primary_key = True)
    disease_id = models.ForeignKey(ConsultantDiseaseTable, to_field ='disease_id', on_delete=models.CASCADE)
    specality_name = models.CharField(max_length = 200, null = True, blank = True)
    specality_description = models.CharField(max_length = 400, null = True, blank = True)

    class Meta:
        db_table = 'specality_master_table'

class DoctorsMastertable(models.Model):

    doctor_id = models.AutoField(unique = True, primary_key = True)
    specality_id = models.ForeignKey(SpecalityMastertable, to_field ='specality_id', on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 200, null=True, blank = True)
    last_name = models.CharField(max_length = 200, null = True, blank = True)
    experience = models.FloatField(null = True, blank = True)
    address1 = models.CharField(max_length = 300, null = True, blank = True)
    city = models.CharField(max_length = 100, null =True, blank = True)
    state = models.CharField(max_length = 50, null = True, blank = True)
    zip_code = models.CharField(max_length = 100, null = True, blank = True)
    
    class Meta:
        db_table = 'doctors_master_table'


class TimeSlottable(models.Model):

    doctor_id = models.AutoField(unique = True, primary_key = True)
    start_time = models.TimeField('Show start time')
    duration = models.DurationField('Duration od time')
    end_time = models.TimeField("end time", blank=True, null=True)

    class Meta:
        db_table = 'doctors_time_slots_table'

# class Booking_Table(models.Model):

#     booking_iD = models.IntegerField()
#     user_ID = models.AutoField(primary_key=True)
#     physician_ID = models.IntegerField()
#     booking_date = models.DateField()
#     slot_time = models.TimeField()
#     patient_ID = models.IntegerField()
#     specality_ID = models.CharField(max_length=20) 


# class Patient_Record_table(models.Model):
#     patient_record_ID = models.CharField(max_length=20)
#     patient_ID = models.IntegerField()
#     RecordName = models.CharField(max_length=20)
#     Date = models.DateField(auto_now_add=False, auto_now=False, null= True)
#     file_name = models.CharField(max_length=20)
#     file_path_upload = models.FileField(upload_to='documents/%Y/%m/%d/')
#     upadted_date = models.DateField()



