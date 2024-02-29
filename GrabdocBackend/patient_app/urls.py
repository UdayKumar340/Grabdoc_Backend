from django.contrib import admin
from django.urls import path
from patient_app.views import *

urlpatterns = [
    path('mobileregistion/',MobileRegView.as_view()),
    path('verifiy-otp/', verifiyOtp.as_view()),

    path('resend-otp/', ResendOtpView.as_view()),

    path('login/', PatientLoginView.as_view()),
    path('details/', PatientDetailsUpdate.as_view()),



    path('diseases/', ConsultantDiseasesView.as_view()),

    path('specialities/', SpecialityDoctorsView.as_view()),

    path('doctors/', DoctorsView.as_view()),

    path('doctors/<int:doctor_id>', DoctorsView.as_view()),

    path('doctor_time_slots/<int:doctor_id>',Doctors_slot_View.as_view()),


    path('patient-summary/<int:patient_schedule_id>',PatientSummaryView.as_view()),

    path('patient-schedule/', PatientScheduleView.as_view()),

    path('patient-reschedule/', PatientRescheduleView.as_view()),

    path('family-members/', FamilyMemberView.as_view()),

    path('file-upload/', FileUploadView.as_view()),

    path ('medical-records/', MedicalRecordView.as_view()),

    path('patient-schedule-medical-records/<int:patient_schedule_id>',PatientScheduleMedicalRecordView.as_view()),

    path('reviews/', ReviewsView.as_view()),
    path('reviews/<int:doctor_id>', ReviewsView.as_view()),

    path('notifications/',NotificationView.as_view()),


    path('userdevice/',UserDeviceView.as_view()),

    path('payments/',PaymentView.as_view()),

    path('payments/<int:payment_id>', PaymentView.as_view()),

    path('agora-token/',AgoraView.as_view()),

]


