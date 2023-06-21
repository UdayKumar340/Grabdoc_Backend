from django.contrib import admin
from django.urls import path
from patient_app.views import *

urlpatterns = [
    path('mobileregistion/',MobileRegView.as_view()),
    path('verifiy-otp/', verifiyOtp.as_view()),
    path('login/', PatientLoginView.as_view()),
    path('details/', PatientDetailsUpdate.as_view()),



    path('diseases/', ConsultantDiseaseTableView.as_view()),

    path('specalities/', SpecalityDoctorsView.as_view()),

    path('doctors/', DoctorsView.as_view()),

    path('doctors/<int:doctor_id>', DoctorsView.as_view()),

    path('doctor_time_slots/<int:doctor_id>',Doctors_slot_View.as_view()),


    path('patient-summary/<int:patient_id>',PatientSummaryView.as_view()),

    path('patient-schedule/', PatientScheduleView.as_view()),

    path('family-members/', FamilyMemberView.as_view()),

    path('file-upload/', FileUploadView.as_view()),

    path ('medical-records/', MedicalRecordView.as_view()),

    path('patient-schedule-medical-records/<int:patient_schedule_id>',PatientScheduleMedicalRecordView.as_view()),

    path('reviews/', ReviewsView.as_view()),

    
       

]


