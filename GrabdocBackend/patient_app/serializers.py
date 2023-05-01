from rest_framework import serializers
from patient_app.models import *


class MobileRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile_Reg
        fields = ['phone_number','device_id','ctime','otp' ]
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)





class PatientMasterTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientMasterTable
        fields =['username', 'email']  
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class ConsultantDiseaseTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsultantDiseaseTable
        fields =['disease_id', 'disease_type']
    
    print("serializer calling")
    def create(self, validated_data):
        print("consultant create")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class SpecalityMastertableSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecalityMastertable
        fields =['disease_id', 'specality_id', 'specality_name', 'specality_description']
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class DoctorsMastertableSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorsMastertable
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class TimeSlottableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSlottable
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)




