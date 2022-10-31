import site
from django.contrib import admin
from doctor_app.models import DoctorInfo
from doctor_app.models import Appointment

# Register your models here.
admin.site.register(DoctorInfo)
admin.site.register(Appointment)
