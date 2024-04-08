
from django.apps import apps
DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots')

"""
from datetime import timedelta
from django.utils import timezone


doctor_ids = [12,16,45]
for doctor_id in doctor_ids:
    a=1
    ds_array=[]
    current_datetime = timezone.now()
    for i in range(a):
        time_slot = timezone.now()
        ds_item = DoctorTimeSlots(doctor_id=doctor_id, time_slot=time_slot)
        print(DoctorTimeSlots(doctor_id=doctor_id))
        ds_array.append(ds_item)
        current_datetime += timedelta(minutes =30)#hours=1

DoctorTimeSlots.objects.bulk_create(ds_array)

#python manage.py shell < ./doctors_app/create_time_slots.py

"""


from django.apps import apps
from datetime import timedelta
from django.utils import timezone

DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots')

doctor_ids = [12, 16, 45]
time_increment = timedelta(minutes=30)  # Adjust as needed

ds_array = []

for doctor_id in doctor_ids:
    current_datetime = timezone.now()
    for _ in range(5):  # Create time slots for 24 hours, adjust as needed
        ds_item = DoctorTimeSlots(doctor_id=doctor_id, time_slot=current_datetime)
        ds_array.append(ds_item)
        current_datetime += time_increment

DoctorTimeSlots.objects.bulk_create(ds_array)



#TODO: select all time slots of today and also repeat = daily 
#2 create a time slot for same time for the date is todays date +7
#