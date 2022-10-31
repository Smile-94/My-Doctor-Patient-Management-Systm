from django import forms
from appointment_app.models import DoctorAppointment, OnlineDoctorAppointment

class DoctorAppointmentForm(forms.ModelForm):
    
    class Meta:
        model = DoctorAppointment
        fields=('appointment_time',)

        widgets={
            'appointment_time':forms.TimeInput(attrs={'class':'timepicker','type':'time','format':'%H:%M','placeholder':'HH:MM:AM'}),
        }

class OnlineDoctorAppointmentForm(forms.ModelForm):
    
    class Meta:
        model = OnlineDoctorAppointment
        fields=('online_appointment_time',)

        widgets={
            'online_appointment_time':forms.TimeInput(attrs={'class':'timepicker','type':'time','format':'%H:%M','placeholder':'HH:MM:AM'}),
        }
