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
        fields = ["patient_first_name","patient_last_name","gendar","email",'date_of_birth'] 
    
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






