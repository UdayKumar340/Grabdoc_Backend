

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 
from django.conf import settings


"""
from django.apps import apps
GrabdocDoctor = apps.get_model('doctors_app', 'GrabdocDoctor') # Doctors
DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots') #DoctorsSchedule
DoctorSpecialities = apps.get_model('doctors_app', 'DoctorSpecialities')#DoctorSpecialities
"""
#class PatientmasterManager(models.Manager):
#   def create(self, *args, **kwargs):
#      print("manager calling..")
#     max_patient_id = PatientMasterTable.objects.latest('patient_id')
#    print("max patient id", max_patient_id)
#    kwargs['patient_id'] =int(max_patient_id)+1 if max_patient_id else 100000
#    super(PatientmasterManager, self).create(*args, **kwargs)


class Mobile_Reg(models.Model):
    phone_number = models.CharField(max_length=15, null= False, blank=False)
    device_id = models.CharField(max_length=100)
    is_phone_verified = models.BooleanField(default = False)
    ctime = models.DateTimeField(auto_now_add=True, blank=True)
    otp = models.PositiveIntegerField(null = True)
    number_of_attements = models.IntegerField(default=0)



class GrabdocUser(AbstractUser): 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    username = models.CharField(('Phone Number'), validators=[phone_regex], max_length=17, unique=True)
    user_types =(
        ('Doctor','Doctor'),
        ('Patient','Patient'),
        ('other','other')
    )
    user_type = models.CharField(max_length=20,choices=user_types,default= 'Patient')

    def __str__(self):
        return f'{self.username} ({self.user_type})'

    USERNAME_FIELD = 'username'


class GrabdocPatient(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
    first_name = models.CharField(max_length= 200, null=True, blank = True) #change first name and last
    last_name = models.CharField(max_length= 200, null=True, blank = True)
    gender = models.CharField(max_length= 200, null=True, blank = True)
    email = models.CharField(max_length= 200, null=True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    height = models.IntegerField(null = True, blank = True)
    weight = models.IntegerField(null = True, blank = True)
    blood_group = models.CharField(max_length=10,null = True, blank = True)
    profile_picture = models.CharField(max_length= 50,null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    USERNAME_FIELD = 'username'


class ConsultantDiseaseTable(models.Model):
    disease_type = models.CharField(max_length = 300, null = True, blank = True)
    def __str__(self):
        return self.disease_type

    class Meta:
        db_table= 'consultant_disease_table'


"""
class SpecialityMastertable(models.Model): #DoctorSpecialities

    speciality_name = models.CharField(max_length = 200, null = True, blank = True)
    speciality_description = models.CharField(max_length = 400, null = True, blank = True)
    def __str__(self):
        return self.speciality_name
   

    class Meta:
        db_table = 'speciality_master_table'


class Doctors(models.Model):
    name = models.CharField(max_length= 200, null=True, blank = True)
    profile_picture = models.CharField(max_length= 50,null=True, blank=True)
    speciality =  models.ForeignKey(SpecialityMastertable, on_delete=models.CASCADE)
    experience = models.IntegerField(null = True, blank = True)
    designation = models.CharField(max_length= 200, null=True, blank = True)
    online = models.BooleanField()
    video_consultation = models.BooleanField(default=True)
    language = models.CharField(max_length= 200, null=True, blank = True)
    location = models.CharField(max_length= 200, null=True, blank = True)
    fee = models.CharField(max_length= 20, null=True, blank = True)
    about_doctor = models.TextField(null=True, blank = True)
    def __str__(self):
        return self.name


class DoctorsSchedule(models.Model):
    doctor = models.ForeignKey(GrabdocDoctor, on_delete=models.CASCADE)
    time_slot = models.DateTimeField(null=True)
    def __str__(self):
        return self.doctor.name
"""

class FamilyMember(models.Model):
    user = models.ForeignKey(GrabdocPatient, on_delete=models.CASCADE)
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
        unique_together = ('user','first_name',"last_name")


class PatientSchedule(models.Model):
    doctor_time_slot = models.ForeignKey('doctors_app.DoctorTimeSlots', on_delete=models.CASCADE)
    user = models.ForeignKey(GrabdocPatient, on_delete=models.CASCADE)
    status_choices =(
        ('Upcoming','Upcoming'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')
    )
    status = models.CharField(max_length=20,choices=status_choices,default= 'Upcoming')
    appointment_for = models.ForeignKey(FamilyMember, on_delete=models.SET_DEFAULT, default=None, null=True)

    def __str__(self):
        return f'{self.id}| {self.doctor_time_slot}| {self.user}'
        

    class Meta:
        unique_together = ('doctor_time_slot', 'user',)



class PatientSummary(models.Model):
    summary = models.TextField(null=True, blank = True)
    patient_schedule =  models.OneToOneField(PatientSchedule, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True, blank=True)




class MedicalRecord(models.Model):
    user = models.ForeignKey(GrabdocPatient, on_delete=models.CASCADE)
    family_member = models.ForeignKey(FamilyMember, on_delete=models.SET_DEFAULT, null=True,default=None)

    record_name = models.CharField(max_length= 50)

    file_name = models.CharField(max_length= 50,null=True, blank=True)

    record_date = models.DateField(null = True, blank = True)
    def __str__(self):
        return f'{self.family_member} {self.record_name} {self.record_date}'
    



    class Meta:
        unique_together = ('user','family_member',"file_name")

class PatientScheduleMedicalRecord(models.Model):

    patient_schedule =  models.ForeignKey(PatientSchedule, on_delete=models.CASCADE)

    medical_record =  models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.patient_schedule} {self.medical_record}'



    class Meta:
        unique_together = ('patient_schedule','medical_record')


class Reviews(models.Model):
    doctor = models.ForeignKey('doctors_app.GrabdocDoctor', on_delete=models.CASCADE,related_name='reviews_doctor')
    user = models.ForeignKey(GrabdocPatient, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank = True)
    rating = models.IntegerField(default=0)
    rating1 = models.IntegerField(default=0)
    rating2 = models.IntegerField(default=0)
    rating3 = models.IntegerField(default=0)
    rating4 = models.IntegerField(default=0)
    review_date = models.DateField(auto_now_add=True, blank = True)

class Notification(models.Model):
    user = models.ForeignKey(GrabdocUser, on_delete=models.CASCADE)
    reference_user =  models.ForeignKey(GrabdocUser, on_delete=models.SET_DEFAULT,related_name='reference_user',default=None,null=True)
    notification_text = models.TextField(null=True, blank = True)
    notification_date  = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return f'{self.user_id} ,{self.notification_text}'

#user d
# user, device_id push_token ctime utime time_zone login_status bollen field

class UserDevice(models.Model):
    user = models.ForeignKey(GrabdocUser, on_delete=models.CASCADE,default=None,null=True)
    device_id= models.CharField(max_length=100)
    push_token = models.CharField(max_length=500,default=None,null=True)
    ctime = models.DateTimeField(auto_now_add=True, blank=True)
    utime = models.DateTimeField(auto_now_add=True, blank=True)
#    time_zone 
    login_status = models.BooleanField(default = False)

class Payments(models.Model):
    user = models.ForeignKey(GrabdocPatient, on_delete=models.CASCADE)
    patient_schedule = models.ForeignKey(PatientSchedule,on_delete=models.SET_DEFAULT,default=None,null=True)
    payment_choices = (
        ('Pay on Visit','pay on Visit'),
        ('Amazon Pay','Amazon Pay'),
        ('Card','Card'),
        ('PayPal','PayPal'),
        ('Skrill','Skrill')
    )
    payment_type = models.CharField(max_length= 12, choices=payment_choices)
    amount = models.FloatField(default=0)
    status_choices =(
        ('Init','Init'),
        ('Success','Success'),
        ('Failed','Failed'),
        ('Processing','Processing'),
        ('Cancelled','Cancelled')


    )
    status = models.CharField(max_length=20,choices=status_choices,default="Init")
    ctime = models.DateTimeField(auto_now_add=True, blank=True)
    utime = models.DateTimeField(auto_now_add=True, blank=True)

