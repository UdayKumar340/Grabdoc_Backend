from django.apps import apps
from datetime import timedelta, datetime
from django.utils import timezone

DoctorTimeSlots = apps.get_model('doctors_app', 'DoctorTimeSlots')

today = datetime.now().date()
rows = DoctorTimeSlots.objects.filter(time_slot__date=today, repeat="Yearly")
print("rows", len(rows))

ds_array = []