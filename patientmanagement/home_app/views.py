from ast import Return
from django.shortcuts import render

# Create your views here.

def index(request):
    data_dic={'title':'Home'}
    return render(request,'home_app/index.html',context=data_dic)

def signUpRequest(request):
    data_dic={'title':'Login|Sign Up'}
    return render(request,'home_app/loginArea.html',context=data_dic)
