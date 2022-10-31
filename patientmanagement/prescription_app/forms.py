from pyexpat import model
from django import forms
from django.forms import ModelForm

from prescription_app.models import Prescription
from prescription_app.models import Reports
from prescription_app.models import Symptoms
from prescription_app.models import ReportFile
from prescription_app.models import OnlinePrescription
from prescription_app.models import OnlineSymptoms
from prescription_app.models import OnlineReports
from prescription_app.models import OnlineReportFile



class PrescriptionForm(forms.ModelForm):
    
    class Meta:
        model = Prescription
        fields = ("medicine_name","morning_time","lunch_time","dinner_time","comments")

class ReportsForm(forms.ModelForm):
    
    class Meta:
        model = Reports
        fields = ("report_name","report_details")

class SymptomsForm(forms.ModelForm):
    
    class Meta:
        model = Symptoms
        fields = ("next_metting_date","blood_pressure","symptoms","suggestions")

class ReportFileForm(forms.ModelForm):

    class Meta:
        model=ReportFile
        fields = ("report_file_name","report_file",)

class OnlinePrescriptionForm(forms.ModelForm):
    
    class Meta:
        model = OnlinePrescription
        fields = ("online_medicine_name","online_morning_time","online_lunch_time","online_dinner_time","online_comments")

class OnlineReportsForm(forms.ModelForm):
    
    class Meta:
        model = OnlineReports
        fields = ("online_report_name","online_report_details")

class OnlineSymptomsForm(forms.ModelForm):
    
    class Meta:
        model = OnlineSymptoms
        fields = ("online_next_metting_date","online_symptoms","online_suggestions")

class OnlineReportFileForm(forms.ModelForm):

    class Meta:
        model=OnlineReportFile
        fields = ("online_report_file_name","online_report_file",)

