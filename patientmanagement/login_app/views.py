from django.shortcuts import get_object_or_404, render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

from django.contrib.auth.models import Group
from django.conf import settings

#Forms and model
from login_app.models import Profile
from login_app.forms import profileForm
from login_app.forms import signUpForm
from patient_app.models import PatientInfo
from patient_app.forms import PatientInfoForm
from doctor_app.models import DoctorInfo
from doctor_app.forms import DoctorInfoForm



#messages
from django.contrib import messages

# Create your views here.

def adminClick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_app:after_login'))

    form=AuthenticationForm()
    data_dic={'title':'Login','form':form}
    return render(request,'login_app/admin/adminLogin.html',context=data_dic)
    

def doctorClick(request):
    form=AuthenticationForm()
    data_dic={'title':'Doctor Login','form':form,}
    return render(request,'login_app/doctor/doctorLogin.html',context=data_dic)

def patientClick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_app:after_login'))

    form=AuthenticationForm()
    data_dic={'title':'Login','form':form}
    return render(request,'login_app/patient/patientLogin.html',context=data_dic)

#Admin Signup Function
def adminSignUp(request):
    form=signUpForm()
    data_dic={'title':'Admin Sign Up','form':form}
    if request.method=='POST':
        form=signUpForm(request.POST) 
        if form.is_valid():
            user=form.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            
            messages.success(request,"Acount created successfully")
            return HttpResponseRedirect(reverse('login_app:admin_login'))
        else:
            messages.warning(request,"Some issue occerd account not created try againg")
            return HttpResponseRedirect(reverse('login_app:admin_arena'))
    return render(request,'login_app/admin/adminSignup.html',context=data_dic)
    
#Doctor Sign Up
def doctorSignup(request):
    form=signUpForm()
    data_dic={'title':'Doctor Sign UP','form':form}

    if request.method=='POST':
        form=signUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            my_admin_group = Group.objects.get_or_create(name='DOCTOR')
            my_admin_group[0].user_set.add(user)

            messages.success(request,"Acount created successfully")
            return HttpResponseRedirect(reverse('login_app:doctor_login'))
        else:
            messages.warning(request,"Some issue occerd account not created try againg")
            return HttpResponseRedirect(reverse('login_app:doctor_signup'))
    return render(request,'login_app/doctor/doctorSignup.html',context=data_dic)

#Patient Signup Function
def patientSignup(request):
    form=signUpForm()
    data_dic={'title':'Patient Sign UP','form':form}

    if request.method=='POST':
        form=signUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            my_admin_group = Group.objects.get_or_create(name='PATIENT')
            my_admin_group[0].user_set.add(user)

            messages.success(request,"Acount created successfully")
            return HttpResponseRedirect(reverse('login_app:patient_login'))
        else:
            messages.warning(request,"Some issue occerd account not created try againg")
            return HttpResponseRedirect(reverse('login_app:patient_signup'))
    return render(request,'login_app/patient/patientSignup.html',context=data_dic)

#Admin Login function           
def loginAdmin(request):

    form=AuthenticationForm()
    data_dic={'title':'Admin Login','form':form}

    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('login_app:admin_info')
    return render(request,'login_app/admin/adminLogin.html',context=data_dic)

#Doctor Login Function
def loginDoctor(request):

    form=AuthenticationForm()
    data_dic={'title':'Doctor Login','form':form}

    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('login_app:doctor_info')
            else:
                messages.warning("Invalid User Name of Password")
    return render(request,'login_app/doctor/doctorLogin.html',context=data_dic)

#Patient login function
def loginPatient(request):

    form=AuthenticationForm()
    data_dic={'title':'Patient Login','form':form}

    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('login_app:patient_info')
            else:
                messages.warning("Invalid User Name of Password")
    return render(request,'login_app/patient/patientLogin.html',context=data_dic)

#admin information function
@login_required
def adminInfo(request):
    profile_qs=Profile.objects.filter(user=request.user)
    profile_qs=profile_qs[0]

    if profile_qs.fullName !="" :
        return HttpResponseRedirect(reverse('login_app:after_login'))
    
    profile=Profile.objects.get(user=request.user)
    profile.user_catagory='ADMIN'
    profile.save()
    form=profileForm(instance=profile)
    if request.method=='POST':
        form=profileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()

            messages.success(request,"Your profile has been update successfully")
            form=profileForm(request.POST,instance=profile)
            return redirect('login_app:after_login')
    return render(request,'login_app/admin/adminInfo.html',context={'form':form,})

#Doctor Information Function
@login_required
def doctorInfo(request):
    profile_qs=Profile.objects.filter(user=request.user)
    profile_qs=profile_qs[0]

    doctor_qs=DoctorInfo.objects.filter(user=request.user)
    print(doctor_qs)
    doctor_qs=doctor_qs[0]

    if profile_qs.fullName !="":
        return HttpResponseRedirect(reverse('login_app:after_login'))
    
    profile=Profile.objects.get(user=request.user)
    profile.user_catagory='DOCTOR'
    profile.save()
    doctor_info=DoctorInfo.objects.get(user=request.user)
    form=profileForm(instance=profile)
    doctor_form=DoctorInfoForm(instance=doctor_info)
    if request.method=='POST':
        form=profileForm(request.POST,request.FILES,instance=profile)
        doctor_form=DoctorInfoForm(request.POST,instance=doctor_info)
        if form.is_valid():
            form.save()
            doctor_form.save()

            messages.success(request,"Your profile has been update successfully")
            form=profileForm(request.POST,instance=profile)
            doctor_form=DoctorInfoForm(request.POST,instance=doctor_info)

            return redirect('login_app:after_login')
    return render(request,'login_app/doctor/doctorInfo.html',context={'title':'doctor Infop','form':form,'doctor_form':doctor_form})

#Patient Information Function
@login_required
def patientInfo(request):
    profile_qs=Profile.objects.filter(user=request.user)
    profile_qs=profile_qs[0]

    patient_qs=PatientInfo.objects.filter(user=request.user)
    patient_qs=patient_qs[0]

    if profile_qs.fullName !="" and patient_qs.age!=0:
        return HttpResponseRedirect(reverse('login_app:after_login'))
    
    profile=Profile.objects.get(user=request.user)
    profile.user_catagory='PATIENT'
    profile.save()
    patient_info=PatientInfo.objects.get(user=request.user)
    form=profileForm(instance=profile)
    patient_form=PatientInfoForm(instance=patient_info)
    if request.method=='POST':
        form=profileForm(request.POST,request.FILES,instance=profile)
        patient_form=PatientInfoForm(request.POST,instance=patient_info)
        if form.is_valid():
            form.save()
            patient_form.save()

            messages.success(request,"Your profile has been update successfully")
            form=profileForm(request.POST,instance=profile)
            patient_form=PatientInfoForm(request.POST,instance=patient_info)

            return redirect('login_app:after_login')
    return render(request,'login_app/patient/patientInfo.html',context={'title':'Patient Info', 'form':form,'patient_form':patient_form})


#for checking user is admin , doctor or patient
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()



def afterlogin_view(request):
    if is_admin(request.user):
        accountapproval=Profile.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return  HttpResponseRedirect(reverse('admin_app:admin_dash'))
        
        return render(request,'login_app/admin/adminAprove.html',context={'title':'Wait for approval'})

    if is_patient(request.user):
        return HttpResponseRedirect(reverse('patient_app:patient_dash'))

    if is_doctor(request.user):
        accountapproval=Profile.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return HttpResponseRedirect(reverse('doctor_app:doctor_dash'))
        
        return render(request,'login_app/doctor/doctorAprove.html',context={'title':'Wait for approval'})
        

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are loged out")
    return HttpResponseRedirect(reverse('home_app:singup_or_login'))


