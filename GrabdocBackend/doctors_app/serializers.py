
from rest_framework import serializers
from doctors_app.models import *

from django.db.models import Avg, F

from django.apps import apps
PatientSchedule = apps.get_model('patient_app', 'PatientSchedule')


PatientScheduleMedicalRecord = apps.get_model('patient_app', 'PatientScheduleMedicalRecord')

PatientSummary = apps.get_model('patient_app', 'PatientSummary')


Reviews = apps.get_model('patient_app', 'Reviews')

Notification = apps.get_model('patient_app', 'Notification')


MedicalRecord = apps.get_model('patient_app', 'MedicalRecord')

class DoctorSpecialitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorSpecialities
        fields =['id','speciality_name', 'speciality_description']


class GrabdocDoctorsSerializer(serializers.ModelSerializer):
    speciality_name = serializers.CharField(source='speciality.speciality_name',read_only=True)
    username = serializers.CharField(source='user.username',read_only=True)
    


    class Meta:
        model = GrabdocDoctor
        read_only_fields = ['id','user_id']
        fields = ["user_id","email","username","name","profile_picture","speciality_id","experience","designation","online","video_consultation","language","location","fee","about_doctor","speciality_name","default_password"] 
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DoctorTimeSlotsSerializer(serializers.ModelSerializer):

    
    patient_schedule_id = serializers.SerializerMethodField(read_only=True)
    def get_patient_schedule_id(self, obj):

        ps= PatientSchedule.objects.filter(doctor_time_slot=obj).first()
        if ps:
            return ps.id
        else:
            return None


    class Meta:
        model = DoctorTimeSlots
        fields = ['patient_schedule_id','time_slot','id','repeat']



class DoctorsScheduleSerializer(serializers.ModelSerializer):

    doctors_name = serializers.CharField(source='doctor_time_slot.doctor',read_only=True)


    patient_name = serializers.SerializerMethodField(read_only=True)
    def get_patient_name(self, obj):
        if obj.appointment_for_id:
            return f"{obj.appointment_for.first_name} {obj.appointment_for.last_name}"
        else:
            return f"{obj.user.first_name} {obj.user.last_name}"


    patient_date_of_birth = serializers.SerializerMethodField(read_only=True)
    def get_patient_date_of_birth(self, obj):
        if obj.appointment_for_id:
            return obj.appointment_for.date_of_birth
        else:
            return obj.user.date_of_birth



    patient_profile_picture = serializers.SerializerMethodField(read_only=True)
    def get_patient_profile_picture(self, obj):
        if obj.appointment_for_id:
            return obj.appointment_for.profile_picture
        else:
            return obj.user.profile_picture


    doctor_experience = serializers.CharField(source='doctor_time_slot.doctor.experience',read_only=True)
    doctor_designation = serializers.CharField(source='doctor_time_slot.doctor.designation',read_only=True)
    doctor_speciality = serializers.CharField(source='doctor_time_slot.doctor.speciality',read_only=True)
    doctor_id = serializers.CharField(source='doctor_time_slot.doctor_id',read_only=True)
    time_slot = serializers.CharField(source='doctor_time_slot.time_slot',read_only=True)
    


    class Meta:
        model = PatientSchedule
        fields = [
            'id',"doctors_name",'patient_name','status',
            'doctor_experience','doctor_designation','doctor_speciality','doctor_id','time_slot',
            "patient_profile_picture","patient_date_of_birth"
        ]


class PatientScheduleMedicalRecordSerializer(serializers.ModelSerializer):
    
#    family_member_name = serializers.CharField(source='family_member.relationship',read_only=True)

    record_name=  serializers.CharField(source='medical_record.record_name',read_only=True)
    file_name= serializers.CharField(source='medical_record.file_name',read_only=True)
    record_date=  serializers.CharField(source='medical_record.record_date',read_only=True)




    class Meta:
        model = PatientScheduleMedicalRecord
        fields = ['record_name','file_name','record_date','medical_record_id','patient_schedule_id']




class PatientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSummary
        fields = ['summary','patient_schedule_id','ctime']


class ReviewsSerializer(serializers.ModelSerializer):


    patient_name = serializers.SerializerMethodField(read_only=True)
    def get_patient_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"



    class Meta:
        model = Reviews
        fields = ['doctor_id','user_id','comment','rating','review_date','patient_name']



class NotificationSerializer(serializers.ModelSerializer):

    profile_picture= serializers.SerializerMethodField(read_only=True)

    def get_profile_picture(self, obj):
        return None
#we need deside notification type which image doctor or system image
    class Meta:
        model = Notification
        fields = ['user_id','notification_text','notification_date','reference_user_id','profile_picture']