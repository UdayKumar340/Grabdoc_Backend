from django.apps import apps
from datetime import timedelta, datetime
from django.utils import timezone

DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots')

today = datetime.now().date()
rows = DoctorTimeSlots.objects.filter(time_slot__date=today, repeat="Monthly on the First Monday")
print("rows", len(rows))

ds_array = []

for row in rows:
    # Find the first Monday of the next month
    next_month = today.replace(day=1) + timedelta(days=31)
    next_month = next_month.replace(day=1)
    while next_month.weekday() != 0:  # Monday
        next_month += timedelta(days=1)

    new_time_slot = datetime.combine(next_month, row.time_slot.time())  # Combine date with time

    # Check if the time slot already exists
    if DoctorTimeSlots.objects.filter(doctor_id=row.doctor_id, time_slot=new_time_slot, repeat="Monthly on the First Monday").exists():
        continue

    ds_item = DoctorTimeSlots(doctor_id=row.doctor_id, time_slot=new_time_slot, repeat=row.repeat)
    ds_array.append(ds_item)

DoctorTimeSlots.objects.bulk_create(ds_array)
