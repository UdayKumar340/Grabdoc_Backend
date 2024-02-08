
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