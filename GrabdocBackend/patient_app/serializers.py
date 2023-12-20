
from rest_framework import serializers
from patient_app.models import *

from django.db.models import Avg, F


from django.apps import apps
GrabdocDoctor = apps.get_model('doctors_app', 'GrabdocDoctor') # Doctors
DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots') #DoctorsSchedule
DoctorSpecalities = apps.get_model('doctors_app', 'DoctorSpecalities')#DoctorSpecalities




class MobileRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile_Reg
        fields = ['id','phone_number','device_id','otp' ]
    def create(self, validated_data):

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



#change PMTS to gus is done
# patint_id change to user_id  done


class GrabdocPatientSerializer(serializers.ModelSerializer): #PatientMasterTableSerializer
    phonenumber = serializers.CharField(source='user.username',read_only=True)


    class Meta:
        model = GrabdocPatient
        read_only_fields = ["phonenumber",'user_id',]
        fields = ['user_id',"first_name","last_name","gender","email",'date_of_birth','height','weight','blood_group',"phonenumber"] 
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class ConsultantDiseaseTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsultantDiseaseTable
        fields =['id','disease_type']
    


class SpecalityMastertableSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorSpecalities
        fields =['id','specality_name', 'specality_description']


class DoctorsSerializer(serializers.ModelSerializer):

    specality_name = serializers.CharField(source='specality.specality_name', read_only=True)

    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, obj):
        return Reviews.objects.filter(doctor=obj).aggregate(avgs=Avg(F('rating'))).get('avgs',None)
    
        #return obj.album_set.aggregate(avgs=Avg(F('num_stars'))).get('avgs',None)

    id = serializers.IntegerField(source='user_id',read_only=True)
    class Meta:
        model = GrabdocDoctor
        fields = ['id','name',"profile_picture",'specality_id','specality_name','experience','designation','online','language','location','about_doctor',"fee",'rating','video_consultation']

class DoctorsScheduleSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(source='doctor.name',read_only=True)



    class Meta:
        model = DoctorTimeSlots
        fields = ['doctor_id','doctor_name','time_slot','id']


class PatientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSummary
        fields = ['summary','user_id']


class PatientScheduleSerializer(serializers.ModelSerializer):
    doctors_name = serializers.CharField(source='doctor_time_slot.doctor.name',read_only=True)

    patient_first_name = serializers.CharField(source='user.first_name',read_only=True)
    patient_last_name = serializers.CharField(source='user.last_name',read_only=True)

    doctor_experience = serializers.CharField(source='doctor_time_slot.doctor.experience',read_only=True)
    doctor_designation = serializers.CharField(source='doctor_time_slot.doctor.designation',read_only=True)
    doctor_specality = serializers.CharField(source='doctor_time_slot.doctor.specality',read_only=True)
    doctor_id = serializers.CharField(source='doctor_time_slot.doctor_id',read_only=True)
    time_slot = serializers.CharField(source='doctor_time_slot.time_slot',read_only=True)
    



    class Meta:
        model = PatientSchedule
        fields = ["doctor_time_slot_id","doctors_name","user_id",'patient_first_name',"patient_last_name",'status','doctor_experience','doctor_designation','doctor_specality','doctor_id','time_slot']


class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = ['id','profile_picture','user_id','first_name','last_name','gender','date_of_birth','relationship']



class MedicalRecordSerializer(serializers.ModelSerializer):
    
    family_member_name = serializers.CharField(source='family_member.relationship',read_only=True)


    class Meta:
        model = MedicalRecord
        fields = ["user_id",'family_member_id','family_member_name','record_name','file_name','record_date']





class PatientScheduleMedicalRecordSerializer(serializers.ModelSerializer):

#    patient_schedule = serializers.CharField(source='patient_schedule.patient_schedule', read_only=True)
    


    class Meta:
        model = PatientScheduleMedicalRecord
        fields = ['patient_schedule_id','medical_record_id']


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['doctor_id','user_id','comment','rating','review_date']

class NotificationSerializer(serializers.ModelSerializer):

    profile_picture= serializers.SerializerMethodField(read_only=True)

    def get_profile_picture(self, obj):
        return None
#we need deside notification type which image doctor or system image
    class Meta:
        model = Notification
        fields = ['user_id','notification_text','notification_date','reference_user_id','profile_picture']

class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ['user_id','device_id','push_token']





class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['user_id','patient_schedule_id','payment_type','amount','status','ctime','utime']

