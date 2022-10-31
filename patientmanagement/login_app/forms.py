from django import forms
from django.forms import ModelForm
from login_app.models import User
from login_app.models import Profile

from django.contrib.auth.forms import UserCreationForm

#froms
class profileForm(ModelForm):
    class Meta:
        model=Profile
        fields=('fullName','gender','user_phone','user_photo','status',)
        widgets={
            'fullName':forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}),
            'gender':forms.Select(attrs={'class':'form-control',}),
            'user_phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter phone Number'}),
            'user_photo':forms.FileInput(attrs={'class':'form-control'}),      
        }


class signUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=('email','password1','password2',)
        

        widgets={
            'email':forms.EmailInput(attrs={'class':'form-group','placeholder':'example@domain.com'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password',}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Conform Password'}),       
        }