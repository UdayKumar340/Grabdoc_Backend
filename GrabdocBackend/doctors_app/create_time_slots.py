
from django.apps import apps
DoctorTimeSlots = apps.get_model('patient_app', 'DoctorTimeSlots')

doctor_ids = [12, 40, 36]
for doctor_id in doctor_ids:
    time_slots = []

    for time_slot in time_slots:
        ds_item = DoctorTimeSlots(doctor_id=doctor_id, time_slot=time_slot)
        ds_array.append(ds_item)

    DoctorTimeSlots.objects.bulk_create(ds_array)

#python manage.py shell < ./doctors_app/create_time_slots.py


"""
import requests
import datetime
from datetime import timedelta
headers = {"Authorization":"Token be2f73bd0506f70b64cb0aa3353554c7942a614a"}
base_url = "http://localhost:8000/doctors/time-slots/"
ids = []
for i in ids:
    url = f"{base_url}{i}"
    a=6
    current_datetime = datetime.datetime.now()
    for i in range(a):
        data = {"time_slot":current_datetime.strftime('%Y-%m-%dT%H:%M:%S')}
        r= requests.post(url,headers=headers,json=data)
        print(r.content)
        current_datetime += timedelta(minutes =30)#hours=1

"""