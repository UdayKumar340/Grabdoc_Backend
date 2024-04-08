from django.apps import apps
from datetime import timedelta, datetime
from django.utils import timezone

from doctors_app.views import Doctors_slot_View

DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots')



today = datetime.now().date()
rows = DoctorTimeSlots.objects.filter(time_slot__date=today,repeat ="Daily")
print("rows",len(rows))

ds_array = []

for row in rows:
    new_time_slot = row.time_slot+timedelta(days=7)
    if DoctorTimeSlots.objects.filter(doctor_id=row.doctor_id, time_slot=new_time_slot):
        continue  
    ds_item = DoctorTimeSlots(doctor_id=row.doctor_id, time_slot=new_time_slot, repeat=row.repeat)
    ds_array.append(ds_item)

DoctorTimeSlots.objects.bulk_create(ds_array)

C:\Users\Admin\Documents\GitHub\Grabdoc_Backend\GrabdocBackend\doctors_app\daily_time_slots_cron_job.py

#python manage.py shell < ./doctors_app/time_slots.py
