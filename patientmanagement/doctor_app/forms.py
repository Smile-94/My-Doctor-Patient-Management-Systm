from pyexpat import model
from django import forms
from django.forms import ModelForm
from doctor_app.models import DoctorInfo
from doctor_app.models import Appointment
from doctor_app.models import OnlineAppointment
from django.conf import settings

#forms
class DoctorInfoForm(forms.ModelForm):
    class Meta:
        model=DoctorInfo
        fields=('title','date_of_birth','national_ID_number','passport_number','registration_number_BMDC','doctor_type','specialist','road','sector','city','postcode','doctor_sort_description')

        

        widgets={
            'title':forms.Select(attrs={'class':'form-control',}),
            'date_of_birth':forms.TextInput(attrs={'class':'form-control','type':'date'}),
            'national_ID_number':forms.TextInput(attrs={'class':'form-control',}),
            'passport_number':forms.TextInput(attrs={'class':'form-control',}),
            'registration_number_BMDC':forms.TextInput(attrs={'class':'form-control',}),
            'doctor_type':forms.Select(attrs={'class':'form-control',}),
            'specialist':forms.Select(attrs={'class':'form-control'}),
            'road':forms.TextInput(attrs={'class':'form-control','placeholder':'Road-10'}),
            'sector':forms.TextInput(attrs={'class':'form-control','placeholder':'Uttara-10'}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder':'Dhaka'}),
            'postcode':forms.NumberInput(attrs={'class':'form-control'}),
            'doctor_sort_description':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Details About You'}),     
        }

class AppointmentForm(forms.ModelForm):
    
    class Meta:
        model = Appointment
        fields = ("appointment_date","time_slot","room_number","hospital_name","number_of_patient","active_status")

        widgets={
            'appointment_date':forms.DateInput(attrs={'type':'date'}),
        }

class CancelForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("cancel_message",)

class OnlineAppointmentForm(forms.ModelForm):

    class Meta:
        model=OnlineAppointment
        fields = ("online_appointment_date","online_time_slot","online_number_of_patient","online_active_status","zoom_link",)

        widgets={
            'online_appointment_date':forms.DateInput(attrs={'type':'date'}),
        }

class OnlineCancelForm(forms.ModelForm):
    class Meta:
        model = OnlineAppointment
        fields = ("online_cancel_message",)