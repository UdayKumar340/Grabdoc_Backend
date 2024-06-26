from django.contrib import admin
from django.urls import path
from doctors_app.views import *

urlpatterns = [
    path('specialities/', DoctorsSpecialityView.as_view()),
    path('doctor-details/',DoctorsDetails.as_view()),
    path('login/',LoginView.as_view()),
    path('change-password/',ChangePasswordView.as_view()),
    path('time-slots/',Doctors_slot_View.as_view()),
    path('delete-time-slot/', DeleteTimeslot.as_view()),
    path('appointments/', DoctorsScheduleView.as_view()),
    path('patient-schedule-medical-records/<int:patient_schedule_id>', PatientScheduleMedicalRecordView.as_view()),
    path('patient-summary/<int:patient_schedule_id>',PatientSummaryView.as_view()),

    path('reviews/', ReviewsView.as_view()),

    path('notifications/',NotificationView.as_view()),


]