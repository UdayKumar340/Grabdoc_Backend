from django.contrib import admin
from django.urls import path
from patient_app.views import *

urlpatterns = [
    path('mobileregistion/',MobileRegView.as_view()),
    path('verifiy-otp/', verifiyOtp.as_view()),
    path('login/', PatientLoginView.as_view()),
    path('<int:patient_id>', PatientDetailsUpdate.as_view()),

    path('consultantdisease/', ConsultantDiseaseTableView.as_view()),
    path('consultantdisease/<int:consultant_id>/', ConsultantDiseaseTableView.as_view()),
    path('SpecalityMaster/<int:specality_id>/', SpecalityDoctorsView.as_view()),
    path('physician/<int:doctor_id>/', DoctorSlotsView.as_view()),



    #path('physician/<int:doctor_id>/slotbooking/', DoctorSlotsView.as_view()),
    

    

]


