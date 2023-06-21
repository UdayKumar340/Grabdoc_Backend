from django.contrib import admin

# Register your models here.
from patient_app.models import *

admin.site.register(Mobile_Reg)

admin.site.register(PatientMasterTable)


admin.site.register(ConsultantDiseaseTable)

admin.site.register(SpecalityMastertable)

admin.site.register(Doctors)

admin.site.register(DoctorsSchedule)


admin.site.register(PatientSummary)


admin.site.register(PatientSchedule)

admin.site.register(FamilyMember)

admin.site.register(MedicalRecord)

admin.site.register(PatientScheduleMedicalRecord)

admin.site.register(Reviews)