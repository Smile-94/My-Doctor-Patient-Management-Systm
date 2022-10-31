from ast import mod
from django.db import models

from login_app.models import User

#To create automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

# Create your models here.

class DoctorCatagory(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_catagoy=models.CharField(max_length=100)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.doctor_catagoy
    
    class Meta:
        verbose_name_plural="Categories"

