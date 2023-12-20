from django.contrib import admin

# Register your models here.
from doctors_app.models import *


class DoctorSpecalitiesAdmin(admin.ModelAdmin):
  list_display = ("id","specality_name","specality_description")
admin.site.register(DoctorSpecalities, DoctorSpecalitiesAdmin)

class GrabdocDoctorAdmin(admin.ModelAdmin):
  list_display = ("user_id","name","designation","specality","location")

admin.site.register(GrabdocDoctor, GrabdocDoctorAdmin)


class DoctorTimeSlotsAdmin(admin.ModelAdmin):
  list_display = ("id","doctor","time_slot")

admin.site.register(DoctorTimeSlots, DoctorTimeSlotsAdmin)


