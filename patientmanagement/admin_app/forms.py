from pyexpat import model
from django import forms
from django.forms import ModelForm

from admin_app.models import DoctorCatagory

#froms
class DoctorCatagoryForm(forms.ModelForm):

    class Meta:
        model=DoctorCatagory
        fields=('doctor_catagoy',)

        widgets={
            'doctor_catagoy':forms.TextInput(attrs={'class':'form-control','placeholder':'Neurologists'}),
                 
        }

