from ast import mod
from django.db import models

#inherit models
from login_app.models import User


#To create automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
marriage_info=(('Married','Married'),('Unmarrid','Unmarrid'))
class PatientInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient_info')
    age=models.IntegerField(default=0)
    village=models.CharField(max_length=50,blank=True)
    post_office=models.CharField(max_length=50,blank=True)
    police_station=models.CharField(max_length=50,blank=True)
    district=models.CharField(max_length=50,blank=True)
    post_code=models.IntegerField(blank=True,default=0000)
    marital_status=models.CharField(max_length=10,choices=marriage_info,default='No')

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        PatientInfo.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()


