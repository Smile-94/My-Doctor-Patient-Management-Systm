from typing import Tuple
from django.db import models
from login_app.models import User
from appointment_app.models import OnlineDoctorAppointment

# Create your models here.

class PaymentStatus(models.Model):
    payment_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='payment')
    payment_appointment=models.ForeignKey(OnlineDoctorAppointment,on_delete=models.CASCADE,default=None)
    tran_id=models.CharField(max_length=300,blank=True,null=True,default=None)
    valid_id=models.CharField(max_length=300,blank=True,null=True,default=None)
    payment_status=models.BooleanField(default=False)
    payment_date=models.DateField(auto_now_add=True)

