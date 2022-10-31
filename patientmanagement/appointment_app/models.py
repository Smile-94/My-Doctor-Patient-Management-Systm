from urllib import request
from django.db import models
from login_app.models import User
from doctor_app.models import Appointment, OnlineAppointment
from django.conf import settings
from datetime import datetime, time

default_time=datetime.now()
# Create your models here.

class DoctorAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_d=models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor_det')
    patient_d=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='patient_det')
    appointment_d=models.ForeignKey(Appointment,on_delete=models.CASCADE,related_name='appoint_det')
    appointment_status=models.BooleanField(default=False)
    added_to_appoint=models.BooleanField(default=False)
    report_status=models.BooleanField(default=False)
    appointment_time=models.TimeField(auto_now_add=False,blank=True,null=True,)
    serial_number=models.IntegerField(default=1)

class OnlineDoctorAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    online_doctor_d=models.ForeignKey(User,on_delete=models.CASCADE,related_name='online_doctor')
    online_patient_d=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='online_patient')
    online_appointment_d=models.ForeignKey(OnlineAppointment,on_delete=models.CASCADE,related_name='online_appoint')
    online_appointment_status=models.BooleanField(default=False)
    online_report_status=models.BooleanField(default=False)
    online_appointment_time=models.TimeField(auto_now_add=False,blank=True,null=True,)
    online_serial_number=models.IntegerField(default=1)

