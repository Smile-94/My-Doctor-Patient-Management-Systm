from django.contrib import admin
from appointment_app.models import DoctorAppointment
from appointment_app.models import OnlineDoctorAppointment

# Register your models here.
admin.site.register(DoctorAppointment)
admin.site.register(OnlineDoctorAppointment)
