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



    

]


