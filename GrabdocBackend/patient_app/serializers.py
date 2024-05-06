
from rest_framework import serializers
from patient_app.models import *

from django.db.models import Avg, F


from django.apps import apps
GrabdocDoctor = apps.get_model('doctors_app', 'GrabdocDoctor') # Doctors
DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots') #DoctorsSchedule
DoctorSpecialities = apps.get_model('doctors_app', 'DoctorSpecialities')#DoctorSpecialities
ConsultantDiseases = apps.get_model('doctors_app', 'ConsultantDiseases')




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
        fields = [
            'user_id',"first_name","last_name","gender","email",'date_of_birth','height',
            'weight','blood_group',"phonenumber","profile_picture"
        ] 
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class ConsultantDiseasesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsultantDiseases
        fields =['id','disease_type']
    


class SpecialityMastertableSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorSpecialities
        fields =['id','speciality_name', 'speciality_description','disease_id']


class DoctorsSerializer(serializers.ModelSerializer):

    speciality_name = serializers.CharField(source='speciality.speciality_name', read_only=True)


    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, obj):
        #return Reviews.objects.filter(doctor=obj).aggregate(avgs=Avg(F('rating'))).get('avgs',None)
        avg_rating = Reviews.objects.filter(doctor=obj).aggregate(avgs=Avg(F('rating'))).get('avgs', None)
        print("avg_rating",avg_rating)
        if avg_rating is not None:
            avg_rating = round(avg_rating, 1)
            print("after round avg_rating",avg_rating)
            return avg_rating
        else:
            return None
    
        #return obj.album_set.aggregate(avgs=Avg(F('num_stars'))).get('avgs',None)
    patient_count = serializers.SerializerMethodField(read_only=True)

    def get_patient_count(self,obj):
        return PatientSchedule.objects.filter(doctor_time_slot__doctor = obj).count()


    id = serializers.IntegerField(source='user_id',read_only=True)
    class Meta:
        model = GrabdocDoctor
        fields = [
            'id','name',"profile_picture",'speciality_id','speciality_name',
            'experience','designation','online','language','location','about_doctor',"fee",
            'rating','video_consultation','patient_count'
        ]

class DoctorsScheduleSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(source='doctor.name',read_only=True)



    class Meta:
        model = DoctorTimeSlots
        fields = ['doctor_id','doctor_name','time_slot','id']


class PatientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSummary
        fields = ["id",'summary','patient_schedule_id','ctime']
        read_only_fields = ['patient_schedule_id', 'ctime']


class PatientScheduleSerializer(serializers.ModelSerializer):
    doctors_name = serializers.CharField(source='doctor_time_slot.doctor.name',read_only=True)
    doctor_experience = serializers.CharField(source='doctor_time_slot.doctor.experience',read_only=True)
    doctor_designation = serializers.CharField(source='doctor_time_slot.doctor.designation',read_only=True)
    doctor_speciality = serializers.CharField(source='doctor_time_slot.doctor.speciality',read_only=True)
    doctor_profile_picture= serializers.CharField(source='doctor_time_slot.doctor.profile_picture',read_only=True)
    doctor_id = serializers.CharField(source='doctor_time_slot.doctor_id',read_only=True)
    time_slot = serializers.CharField(source='doctor_time_slot.time_slot',read_only=True)

    doctor_rating = serializers.SerializerMethodField(read_only=True)
    def get_doctor_rating(self,obj):
        avg_rating =  Reviews.objects.filter(doctor_id=obj.doctor_time_slot.doctor_id).aggregate(avgs=Avg(F('rating'))).get('avgs',None)
        if avg_rating is not None:
            avg_rating = round(avg_rating, 1)
            print("after round avg_rating in patient scs",avg_rating)
            return avg_rating
        else:
            return None

    appointment_for_name = serializers.SerializerMethodField(read_only=True)
    def get_appointment_for_name(self, obj):
        if obj.appointment_for_id:
            return f"{obj.appointment_for.first_name} {obj.appointment_for.last_name} ({obj.appointment_for.relationship})"
        else:
            print('user_id:', obj.user_id)
            print('first_name:', obj.user.first_name)
            print('last_name:', obj.user.last_name)
            return f"{obj.user.first_name} {obj.user.last_name} (Myself)"
            
    class Meta:
        model = PatientSchedule
        fields = [ 
           "id", "doctor_time_slot_id", "doctors_name", "user_id", 
            'appointment_for_name', 'status', 'doctor_experience',
            'doctor_designation', 'doctor_speciality', 'doctor_id', 'time_slot','doctor_rating',"doctor_profile_picture"
        ]

class FamilyMemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FamilyMember
        fields = ['id','profile_picture','user_id','first_name','last_name','gender','date_of_birth','relationship']



class MedicalRecordSerializer(serializers.ModelSerializer):
    
    family_member_name = serializers.CharField(source='family_member.relationship',read_only=True)


    class Meta:
        model = MedicalRecord
        fields = ["id","user_id",'family_member_id','family_member_name','record_name','file_name','record_date']





class PatientScheduleMedicalRecordSerializer(serializers.ModelSerializer):

#    patient_schedule = serializers.CharField(source='patient_schedule.patient_schedule', read_only=True)
    


    class Meta:
        model = PatientScheduleMedicalRecord
        fields = ['patient_schedule_id','medical_record_id']


class ReviewsSerializer(serializers.ModelSerializer):

    patient_name = serializers.SerializerMethodField(read_only=True)
    def get_patient_name(self, obj):
            return f"{obj.user.first_name} {obj.user.last_name}"
    
    profile_picture = serializers.CharField(source='user.profile_picture',read_only=True)
    



    class Meta:
        model = Reviews
        fields = [
            'id','doctor_id','user_id','comment','rating',
            'review_date',"rating1","rating2","rating3","rating4","patient_name",
            'profile_picture'
        ]

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

