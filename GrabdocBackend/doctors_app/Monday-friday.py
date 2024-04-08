from django.apps import apps
from datetime import timedelta, datetime
from django.utils import timezone

DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots')

today = datetime.now().date()
rows = DoctorTimeSlots.objects.filter(time_slot__date=today, repeat="Every Week (Monday to Friday)")
print("rows", len(rows))

ds_array = []

# Define the range of days (Monday to Friday)
start_day = 0  # Monday (0-indexed)
end_day = 4    # Friday (0-indexed)

for row in rows:
    for day_offset in range(start_day, end_day + 1):
        new_time_slot = row.time_slot + timedelta(days=day_offset)
        if DoctorTimeSlots.objects.filter(doctor_id=row.doctor_id, time_slot=new_time_slot, repeat="Every Week (Monday to Friday)").exists():
            continue
        ds_item = DoctorTimeSlots(doctor_id=row.doctor_id, time_slot=new_time_slot, repeat=row.repeat)
        ds_array.append(ds_item)

DoctorTimeSlots.objects.bulk_create(ds_array)
