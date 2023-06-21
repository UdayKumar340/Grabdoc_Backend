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
    phonenumber = serializers.CharField(source='username',read_only=True)


    class Meta:
        model = PatientMasterTable
        read_only_fields = ["phonenumber",'id',]
        fields = ['id',"patient_first_name","patient_last_name","gendar","email",'date_of_birth','height','weight','blood_group',"phonenumber"] 
    
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

    specality_name = serializers.CharField(source='specality.specality_name', read_only=True)
 

    class Meta:
        model = Doctors
        fields = ['id','name',"profile_picture",'specality_id','specality_name','experience','designation','online','language','location','about_doctor',"fee"]

class DoctorsScheduleSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(source='doctor.name',read_only=True)



    class Meta:
        model = DoctorsSchedule
        fields = ['doctor_id','doctor_name','time_slot']


class PatientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSummary
        fields = ['summary','patient_id']


class PatientScheduleSerializer(serializers.ModelSerializer):
    doctors_name = serializers.CharField(source='doctors_schedule.doctor',read_only=True)

    patient_first_name = serializers.CharField(source='patient.patient_first_name',read_only=True)
    patient_last_name = serializers.CharField(source='patient.patient_last_name',read_only=True)



    class Meta:
        model = PatientSchedule
        fields = ["doctors_schedule_id","doctors_name","patient_id",'patient_first_name',"patient_last_name"]


class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = ['profile_picture','patient_id','first_name','last_name','gender','date_of_birth','relationship']



class MedicalRecordSerializer(serializers.ModelSerializer):
    
    family_menber_name = serializers.CharField(source='family_member.relationship',read_only=True)


    class Meta:
        model = MedicalRecord
        fields = ["patient_id",'family_member_id','family_menber_name','record_name','file_name','record_date']





class PatientScheduleMedicalRecordSerializer(serializers.ModelSerializer):

#    patient_schedule = serializers.CharField(source='patient_schedule.patient_schedule', read_only=True)
    


    class Meta:
        model = PatientScheduleMedicalRecord
        fields = ['patient_schedule_id','medical_record_id']


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['doctor_id','patient_id','comment','rating','review_date']