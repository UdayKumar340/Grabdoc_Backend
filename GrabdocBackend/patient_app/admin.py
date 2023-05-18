from django.contrib import admin

# Register your models here.
from patient_app.models import *

admin.site.register(Mobile_Reg)

admin.site.register(PatientMasterTable)


admin.site.register(ConsultantDiseaseTable)

admin.site.register(SpecalityMastertable)

admin.site.register(Doctors)

admin.site.register(DoctorsSchedule)