from rest_framework import serializers
from patient_app.models import *


class MobileRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile_Reg
        fields = ['id','phone_number','device_id','otp' ]
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)







class PatientMasterTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientMasterTable
        fields = ['id',"patient_first_name","patient_last_name","gendar","email",'date_of_birth','height','weight','blood_group'] 
    
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
        model = SpecalityMastertable
        fields =['id','specality_name', 'specality_description']


class DoctorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctors
        fields = ['id','name','specality','experience','online','language','location','about_doctor']

class DoctorsScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsSchedule
        fields = ['doctor_id','time_slot']


class PatientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSummary
        fields = ['summary','patient_id']


class PatientScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSchedule
        fields = ["doctors_schedule_id","patient_id"]


class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = ['profile_picture','patient_id','first_name','last_name','gender','date_of_birth','relationship']

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ["patient_id",'family_member_id','record_name','file_name','record_date']

class PatientScheduleMedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientScheduleMedicalRecord
        fields = ['patient_schedule_id','medical_record_id']
