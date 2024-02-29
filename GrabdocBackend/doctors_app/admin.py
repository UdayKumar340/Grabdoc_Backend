from django.contrib import admin

# Register your models here.
from doctors_app.models import *


class ConsultantDiseasesAdmin(admin.ModelAdmin):
  list_display = ("id", "disease_type")
admin.site.register(ConsultantDiseases,ConsultantDiseasesAdmin)


class DoctorSpecialitiesAdmin(admin.ModelAdmin):
  list_display = ("id","speciality_name","speciality_description")
admin.site.register(DoctorSpecialities, DoctorSpecialitiesAdmin)

class GrabdocDoctorAdmin(admin.ModelAdmin):
  list_display = ("user_id","name","designation","speciality","location")

admin.site.register(GrabdocDoctor, GrabdocDoctorAdmin)


class DoctorTimeSlotsAdmin(admin.ModelAdmin):
  list_display = ("id","doctor","time_slot")

admin.site.register(DoctorTimeSlots, DoctorTimeSlotsAdmin)


