from django.db import models
from appointment_app.models import DoctorAppointment, OnlineDoctorAppointment
# Create your models here.

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    prescription_for=models.ForeignKey(DoctorAppointment,on_delete=models.CASCADE,related_name='prescription')
    medicine_name=models.CharField(max_length=100)
    morning_time=models.IntegerField(blank=True,null=True,default=0)
    lunch_time=models.IntegerField(blank=True,null=True,default=0)
    dinner_time=models.IntegerField(blank=True,null=True,default=0)
    comments=models.CharField(max_length=150,blank=True,null=True)

class OnlinePrescription(models.Model):
    id = models.AutoField(primary_key=True)
    Online_prescription_for=models.ForeignKey(OnlineDoctorAppointment,on_delete=models.CASCADE,related_name='online_prescription')
    online_medicine_name=models.CharField(max_length=100)
    online_morning_time=models.IntegerField(blank=True,null=True,default=0)
    online_lunch_time=models.IntegerField(blank=True,null=True,default=0)
    online_dinner_time=models.IntegerField(blank=True,null=True,default=0)
    online_comments=models.CharField(max_length=150,blank=True,null=True)

class Reports(models.Model):
    id = models.AutoField(primary_key=True)
    report_for=models.ForeignKey(DoctorAppointment,on_delete=models.CASCADE,related_name='report')
    report_name=models.CharField(max_length=200,)
    report_details=models.CharField(max_length=200,blank=True,null=True)

class OnlineReports(models.Model):
    id = models.AutoField(primary_key=True)
    online_report_for=models.ForeignKey(OnlineDoctorAppointment,on_delete=models.CASCADE,related_name='online_report')
    online_report_name=models.CharField(max_length=200,)
    online_report_details=models.CharField(max_length=200,blank=True,null=True)
    

class Symptoms(models.Model):
    id = models.AutoField(primary_key=True)
    symptoms_for=models.OneToOneField(DoctorAppointment,on_delete=models.CASCADE,related_name='symptoms')
    next_metting_date=models.CharField(max_length=200,blank=True,null=True,default='N/A')
    blood_pressure=models.CharField(max_length=20,blank=True,null=True,default='N/A')
    symptoms=models.TextField(max_length=300,blank=True,null=True,default='N/A')
    suggestions=models.TextField(max_length=300,blank=True,null=True,default='N/A')

    def __str__(self) -> str:
        return str(self.symptoms_for)

class OnlineSymptoms(models.Model):
    id = models.AutoField(primary_key=True)
    online_symptoms_for=models.OneToOneField(OnlineDoctorAppointment,on_delete=models.CASCADE,related_name='online_symptoms')
    online_next_metting_date=models.CharField(max_length=200,blank=True,null=True,default='N/A')
    online_symptoms=models.TextField(max_length=300,blank=True,null=True,default='N/A')
    online_suggestions=models.TextField(max_length=300,blank=True,null=True,default='N/A')

    def __str__(self) -> str:
        return str(self.online_symptoms_for)

class ReportFile(models.Model):
    id = models.AutoField(primary_key=True)
    file_for=models.ForeignKey(DoctorAppointment,on_delete=models.CASCADE,related_name='report_file')
    report_file_name=models.CharField(max_length=200)
    report_file=models.FileField(upload_to='folder')
    report_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.report_file_name

class OnlineReportFile(models.Model):
    id = models.AutoField(primary_key=True)
    online_file_for=models.ForeignKey(OnlineDoctorAppointment,on_delete=models.CASCADE,related_name='online_report_file')
    online_report_file=models.FileField(upload_to='folder')
    online_report_date=models.DateField(auto_now_add=True)
    online_report_file_name=models.CharField(max_length=200)

    def __str__(self):
        return self.online_report_file_name


