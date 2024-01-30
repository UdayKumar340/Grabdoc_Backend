
from django.contrib import admin

# Register your models here.
from patient_app.models import *


class Mobile_RegAdmin(admin.ModelAdmin):
  list_display = ("id", "phone_number", "device_id","otp","number_of_attements",)
  
admin.site.register(Mobile_Reg, Mobile_RegAdmin)

class GrabdocUserAdmin(admin.ModelAdmin):
  list_display = ("id", "username", "user_type",)
admin.site.register(GrabdocUser,GrabdocUserAdmin)


class GrabdocPatientAdmin(admin.ModelAdmin):
  list_display = ("user_id", "first_name", "last_name","gender",)
admin.site.register(GrabdocPatient,GrabdocPatientAdmin)



class ConsultantDiseaseTableAdmin(admin.ModelAdmin):
  list_display = ("id", "disease_type")
admin.site.register(ConsultantDiseaseTable,ConsultantDiseaseTableAdmin)

#admin.site.register(SpecalityMastertable)

#admin.site.register(Doctors)

#admin.site.register(DoctorsSchedule)

class PatientSummaryAdmin(admin.ModelAdmin):
  list_display = ("patient_schedule", "summary","ctime")
admin.site.register(PatientSummary,PatientSummaryAdmin)



class PatientScheduleAdmin(admin.ModelAdmin):
  list_display = ("user_id", "doctor_time_slot","status")
admin.site.register(PatientSchedule,PatientScheduleAdmin)




class FamilyMemberAdmin(admin.ModelAdmin):
  list_display = ("user_id", "first_name","last_name","date_of_birth","gender","relationship")
admin.site.register(FamilyMember,FamilyMemberAdmin)


class MedicalRecordAdmin(admin.ModelAdmin):
  list_display = ("user_id", "user", "family_member","record_name","file_name","record_date")
admin.site.register(MedicalRecord, MedicalRecordAdmin)



class PatientScheduleMedicalRecordAdmin(admin.ModelAdmin):
  list_display = ("id", "patient_schedule", "medical_record")
admin.site.register(PatientScheduleMedicalRecord, PatientScheduleMedicalRecordAdmin)


class ReviewsAdmin(admin.ModelAdmin):
  list_display = ("id", "user", "doctor","comment","rating","review_date")
admin.site.register(Reviews, ReviewsAdmin)

class NotificationAdmin(admin.ModelAdmin):
  list_display = ("id", "user", "notification_text","notification_date","reference_user",)
  
admin.site.register(Notification, NotificationAdmin)



#class UserDeviceAdmin(admin.ModelAdmin):
#  list_display = ("id", "user", "device_id","push_token","reference_user",)
admin.site.register(UserDevice)


admin.site.register(Payments)

