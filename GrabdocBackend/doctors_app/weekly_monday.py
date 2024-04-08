from django.apps import apps
from datetime import timedelta, datetime
from django.utils import timezone

DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots')

today = datetime.now().date()
rows = DoctorTimeSlots.objects.filter(time_slot__date=today, repeat="Weekly on Monday")
print("rows", len(rows))

ds_array = []

for row in rows:
    # Find the next Monday
    next_monday = today + timedelta((0 - today.weekday() + 7) % 7)
    new_time_slot = datetime.combine(next_monday, row.time_slot.time())  # Combine date with time

    # Check if the time slot already exists
    if DoctorTimeSlots.objects.filter(doctor_id=row.doctor_id, time_slot=new_time_slot, repeat="Weekly on Monday").exists():
        continue

    ds_item = DoctorTimeSlots(doctor_id=row.doctor_id, time_slot=new_time_slot, repeat=row.repeat)
    ds_array.append(ds_item)

DoctorTimeSlots.objects.bulk_create(ds_array)
