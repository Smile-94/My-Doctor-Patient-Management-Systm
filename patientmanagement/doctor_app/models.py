from django.db import models
from login_app.models import User
from admin_app.models import DoctorCatagory
from datetime import date
from django.conf import settings

#To create automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

dr_title=(('Dr','Dr'),('Prof Dr','Prof Dr'),('Assoc Prof Dr','Assoc Prof Dr'),('Asst Prof Dr','Asst Prof Dr'))
dr_type=(('Medical','Medical'),('Dental','Dental'))
class DoctorInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='doctor')
    title=models.CharField(max_length=30,choices=dr_title,default='Dr')
    date_of_birth=models.DateField(default=date.today)
    national_ID_number=models.CharField(max_length=50)
    passport_number=models.CharField(max_length=50,blank=True)
    registration_number_BMDC=models.CharField(max_length=50)
    doctor_type=models.CharField(max_length=20,choices=dr_type,default='Medical')
    specialist=models.ForeignKey(DoctorCatagory,on_delete=models.SET_NULL, related_name='specialist',null=True,blank=True)
    road=models.CharField(max_length=50,blank=True)
    sector=models.CharField(max_length=50,blank=True)
    city=models.CharField(max_length=50,blank=True)
    postcode=models.IntegerField(blank=True,default=1230)
    doctor_sort_description=models.TextField(max_length=500,blank=True)

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        DoctorInfo.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()


slot=(
    ('Morning(9.00am-1.00pm)','Morning(9.00am-1.00pm)'),
    ('Afternoon(4.00pm-6.30pm)','Afternoon(4.00pm-6.00pm)'),
    ('Evening(7.30pm-8.30pm)','Evening(7.30pm-8.30pm)'),
    )
active=(
    ('ACTIVE','ACTIVE'),
    ('DEACTIVE','DEACTIVE'),
)
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    appoint_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='appointment')
    appointment_date=models.DateField(default=date.today)
    time_slot=models.CharField(max_length=50,choices=slot,default='Morning(9.00am-1.00am)')
    room_number=models.IntegerField(default=0)
    hospital_name=models.CharField(max_length=200)
    number_of_patient=models.IntegerField(default=1)
    active_status=models.CharField(max_length = 10,choices=active,default='ACTIVE')
    cancel_status=models.BooleanField(default=False)
    cancel_message=models.CharField(max_length=200,default=None,blank=True,null=True)

class OnlineAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    appointment_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='onlineAppointment')
    online_appointment_date=models.DateField(default=date.today)
    online_time_slot=models.CharField(max_length=50,choices=slot,default='Morning(9.00am-1.00am)')
    zoom_link=models.URLField(max_length=300,blank=True,null=True)
    online_number_of_patient=models.IntegerField(default=1)
    online_active_status=models.CharField(max_length = 10,choices=active,default='ACTIVE')
    online_cancel_status=models.BooleanField(default=False)
    online_cancel_message=models.CharField(max_length=200,default=None,blank=True,null=True)

