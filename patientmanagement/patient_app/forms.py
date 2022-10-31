from django import forms
from django.forms import ModelForm

from patient_app.models import PatientInfo


#patient forms
class PatientInfoForm(forms.ModelForm):
    class Meta:
        model=PatientInfo
        fields=('age','village','post_office','police_station','district','post_code','marital_status',)
        widgets={
            'age':forms.NumberInput(attrs={'class':'form-control','placeholder':'Patient Age'}),
            'village':forms.TextInput(attrs={'class':'form-control','placeholder':'Village/Road No'}),
            'postOffice':forms.TextInput(attrs={'class':'form-control','placeholder':'Postoffice/Sector'}),
            'policeStation':forms.TextInput(attrs={'class':'form-control','placeholder':'Police Station'}),
            'district':forms.TextInput(attrs={'class':'form-control','placeholder':'District'}),
            'postCode':forms.NumberInput(attrs={'class':'form-control',}),
            'marital_status':forms.Select(attrs={'class':'form-control',}),     
        }
