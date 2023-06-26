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
    def __str__(self):
        return f'{self.patient_first_name} {self.patient_last_name}'

    

    USERNAME_FIELD = 'username'
#    objects = PatientmasterManager()
#   def __str__(self):
#        return (self.patient_first_name,self.patient_last_name)



class ConsultantDiseaseTable(models.Model):
    disease_type = models.CharField(max_length = 300, null = True, blank = True)
    def __str__(self):
        return self.disease_type

    class Meta:
        db_table= 'consultant_disease_table'

class SpecalityMastertable(models.Model):

    specality_name = models.CharField(max_length = 200, null = True, blank = True)
    specality_description = models.CharField(max_length = 400, null = True, blank = True)
    def __str__(self):
        return self.specality_name
   

    class Meta:
        db_table = 'specality_master_table'


class Doctors(models.Model):
    name = models.CharField(max_length= 200, null=True, blank = True)
    profile_picture = profile_picture = models.CharField(max_length= 50,null=True, blank=True)
    specality =  models.ForeignKey(SpecalityMastertable, on_delete=models.CASCADE)
    experience = models.IntegerField(null = True, blank = True)
    designation = models.CharField(max_length= 200, null=True, blank = True)
    online = models.BooleanField()
    language = models.CharField(max_length= 200, null=True, blank = True)
    location = models.CharField(max_length= 200, null=True, blank = True)
    fee = models.CharField(max_length= 20, null=True, blank = True)
    about_doctor = models.TextField(null=True, blank = True)
    def __str__(self):
        return self.name




class DoctorsSchedule(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    time_slot = models.DateTimeField(null=True)
    def __str__(self):
        return self.doctor.name


class PatientSummary(models.Model):
    summary = models.TextField(null=True, blank = True)
    patient = models.OneToOneField(PatientMasterTable, on_delete=models.CASCADE,primary_key=True)



class PatientSchedule(models.Model):
    doctors_schedule = models.ForeignKey(DoctorsSchedule, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientMasterTable, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.doctors_schedule} {self.patient}'
        

    class Meta:
        unique_together = ('doctors_schedule', 'patient',)


class FamilyMember(models.Model):
    patient = models.ForeignKey(PatientMasterTable, on_delete=models.CASCADE)
    profile_picture = models.CharField(max_length= 50,null=True, blank=True)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    gender = models.CharField(max_length= 10, null=True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    relations_choices = (
        ('Dad','Dad'),
        ('Mom','Mom'),
        ('Husband','Husband'),
        ('Wife','Wife'),
        ('Sister','Sister'),
        ('Brother','Brother'),
        ('Others','Others')
    
    )
    relationship = models.CharField(max_length= 10, choices=relations_choices)

    def __str__(self):
        return self.relationship

    class Meta:
        unique_together = ('patient','first_name',"last_name")



class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientMasterTable, on_delete=models.CASCADE)
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)

    record_name = models.CharField(max_length= 50)

    file_name = models.CharField(max_length= 50,null=True, blank=True)

    record_date = models.DateField(null = True, blank = True)
    def __str__(self):
        return f'{self.family_member} {self.record_name} {self.record_date}'
    





    class Meta:
        unique_together = ('patient','family_member',"file_name")

class PatientScheduleMedicalRecord(models.Model):

    patient_schedule =  models.ForeignKey(PatientSchedule, on_delete=models.CASCADE)

    medical_record =  models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.patient_schedule} {self.medical_record}'



    class Meta:
        unique_together = ('patient_schedule','medical_record')


class Reviews(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE,related_name='reviews_doctor')
    patient = models.ForeignKey(PatientMasterTable, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank = True)
    rating = models.IntegerField(default=0)
    review_date = models.DateField(auto_now_add=True, blank = True)

