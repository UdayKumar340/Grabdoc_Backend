
from rest_framework import serializers
from doctors_app.models import *

from django.db.models import Avg, F

from django.apps import apps
PatientSchedule = apps.get_model('patient_app', 'PatientSchedule')


MedicalRecord = apps.get_model('patient_app', 'MedicalRecord')

PatientSummary = apps.get_model('patient_app', 'PatientSummary')


Reviews = apps.get_model('patient_app', 'Reviews')

Notification = apps.get_model('patient_app', 'Notification')

class DoctorSpecalitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorSpecalities
        fields =['id','specality_name', 'specality_description']


class GrabdocDoctorsSerializer(serializers.ModelSerializer):
    specality_name = serializers.CharField(source='specality.specality_name',read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)


    class Meta:
        model = GrabdocDoctor
        read_only_fields = ['id','user_id']
        fields = ["user_id","email","username","name","profile_picture","specality_id","experience","designation","online","video_consultation","language","location","fee","about_doctor","specality_name","default_password"] 
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DoctorTimeSlotsSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(source='doctor.name',read_only=True)

    class Meta:
        model = DoctorTimeSlots
        fields = ['doctor_id','doctor_name','time_slot','id','repeat']



class DoctorsScheduleSerializer(serializers.ModelSerializer):
    doctors_name = serializers.CharField(source='doctors_schedule.doctor',read_only=True)

    patient_first_name = serializers.CharField(source='user.first_name',read_only=True)
    patient_last_name = serializers.CharField(source='user.last_name',read_only=True)

    doctor_experience = serializers.CharField(source='doctors_schedule.doctor.experience',read_only=True)
    doctor_designation = serializers.CharField(source='doctors_schedule.doctor.designation',read_only=True)
    doctor_specality = serializers.CharField(source='doctors_schedule.doctor.specality',read_only=True)
    doctor_id = serializers.CharField(source='doctors_schedule.doctor_id',read_only=True)
    time_slot = serializers.CharField(source='doctors_schedule.time_slot',read_only=True)
    



    class Meta:
        model = PatientSchedule
        fields = ["doctors_schedule_id","doctors_name","user_id",'patient_first_name',"patient_last_name",'status','doctor_experience','doctor_designation','doctor_specality','doctor_id','time_slot']


class MedicalRecordSerializer(serializers.ModelSerializer):
    
    family_member_name = serializers.CharField(source='family_member.relationship',read_only=True)


    class Meta:
        model = MedicalRecord
        fields = ["user_id",'family_member_id','family_member_name','record_name','file_name','record_date']




class PatientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSummary
        fields = ['summary','patient_schedule_id','ctime']


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