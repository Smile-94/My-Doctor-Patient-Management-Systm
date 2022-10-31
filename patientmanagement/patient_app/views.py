from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.urls import reverse_lazy

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate

from django.contrib.auth.models import Group
from django.conf import settings

#Forms and model
from login_app.models import Profile, User
from login_app.forms import profileForm
from login_app.forms import signUpForm
from patient_app.models import PatientInfo
from patient_app.forms import PatientInfoForm
from doctor_app.models import DoctorInfo, OnlineAppointment
from doctor_app.models import Appointment
from admin_app.models import DoctorCatagory
from appointment_app.models import DoctorAppointment, OnlineDoctorAppointment
from appointment_app.forms import DoctorAppointmentForm
from appointment_app.forms import OnlineDoctorAppointmentForm
from prescription_app.models import OnlinePrescription, OnlineReportFile, OnlineReports, OnlineSymptoms, Prescription
from prescription_app.models import Reports
from prescription_app.models import Symptoms
from prescription_app.models import ReportFile
from payment_app.models import PaymentStatus
from payment_app.forms import PaymentStatusForm


# class based view
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView


#messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
@login_required
def patientDashboard(request):
    data_dic={}
    patient_info=PatientInfo.objects.filter(user=request.user)
    patient_info=patient_info[0]

    #Prescription leatest
    if DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=True).exists():
        appointment_obj=DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=True).latest('doctor_d')
        prescription=Prescription.objects.filter(prescription_for=appointment_obj)
        next_meeting=Symptoms.objects.filter(symptoms_for=appointment_obj)[0]

        prescription_date=prescription[0]
        
        data_dic.update({'medicine_list':prescription,'prescription_date':prescription_date,'next_metting':next_meeting})
   
        
    

    data_dic.update({
        'title':'Patien Dashboard',
        'patient_info':patient_info,
        })
    return render(request,'patient_app/patientDash.html',context=data_dic)

@login_required
def patientProfile(request):
    patient_info=PatientInfo.objects.filter(user=request.user)
    patient_info=patient_info[0]
    data_dic={'title':'My Profile','patient_info':patient_info}
    return render(request,'patient_app/profile.html',context=data_dic)

@method_decorator(login_required,name='dispatch')
class editBasicInfo(SuccessMessageMixin, UpdateView):
    fields=('fullName','gender','user_phone','user_photo')
    model=Profile
    success_url=reverse_lazy('patient_app:patient_profile')
    template_name='patient_app/editBasicInfo.html'
    success_message="Your Basic Information updated successfully"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Edit Basic Info'

        return context

@method_decorator(login_required,name='dispatch')
class editPersonalInfo(SuccessMessageMixin, UpdateView):
    fields=('age','village','post_office','police_station','district','post_code','marital_status',)
    model=PatientInfo
    success_url=reverse_lazy('patient_app:patient_profile')
    template_name='patient_app/editParsonalInfo.html'
    success_message="Your Personal Information updated successfully"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Edit Personal Info'

        return context


@login_required
def findDoctor(request):
    doctor_list=User.objects.filter(groups=2)
    doctor_catagory=DoctorCatagory.objects.all()
    data_dic={'title':'Doctor List','doctor_list':doctor_list,'doctor_catagory':doctor_catagory}
    return render(request,'patient_app/findDoctor.html',context=data_dic)

@login_required
def findDoctorCatagory(request,pk):
    data_dic={'title':'Doctor Catagory'}
    doctor_catagory=DoctorCatagory.objects.all()
    doctor_cata=DoctorInfo.objects.filter(specialist=pk)

    doctor_list=[]
    for catagory in doctor_cata:
        doctor_list.extend(list(User.objects.filter(groups=1,doctor=catagory)) )
    

    data_dic.update({'doctor_list':doctor_list,'doctor_catagory':doctor_catagory})
    
    return render(request,'patient_app/catagoryDoctor.html',context=data_dic)

@login_required
def makeAppointment(request,pk):
    data_dic={}
    form=DoctorAppointmentForm()
    online_form=OnlineDoctorAppointmentForm()
    doctor_details=User.objects.filter(id=pk)
    doctor_details=doctor_details[0]

    appoint_list=Appointment.objects.filter(appoint_user=doctor_details,active_status='ACTIVE',cancel_status=False).order_by('-id')
    online_appoint_list=OnlineAppointment.objects.filter(appointment_user=doctor_details,online_active_status='ACTIVE',online_cancel_status=False)
    data_dic.update({'online_form':online_form,'online_appoint_list':online_appoint_list})
    

    data_dic.update({'title':'Appointment','doctor':doctor_details,'appoint_list':appoint_list,'form':form})
    return render(request,'patient_app/appointment.html',context=data_dic)

@login_required
def confirmAppointment(request,doctor,appointment):
    doctor_obj=User.objects.filter(id=doctor)[0]

    appointments=get_object_or_404(Appointment,pk=appointment)
    appointment_obj_find=DoctorAppointment.objects.filter(patient_d=request.user,doctor_d=doctor_obj,appointment_d=appointments,appointment_status=False)
    number_of_patine=DoctorAppointment.objects.filter(doctor_d=doctor_obj,appointment_d=appointments,appointment_status=False).count()
    # pending_appointment=DoctorAppointment.objects.filter(patient_d=request.user,doctor_d=doctor_obj,appointment_status=False)
   
    if(number_of_patine>=appointments.number_of_patient):
        messages.warning(request,'This slot already booked try another slot')
        return HttpResponseRedirect(reverse('patient_app:find_doctor'))

    elif(appointment_obj_find.exists()):
        messages.warning(request,"You have already appointment on this slot")
        url='/patient/make_appointmnet/{doctor_id}/'.format(doctor_id=doctor)
        return redirect(url)

    else:
        appointment_obj=DoctorAppointment.objects.get_or_create(patient_d=request.user,doctor_d=doctor_obj,appointment_d=appointments)
        appointment_obj=appointment_obj[0]
        appointment_obj.added_to_appoint=True
        appointment_obj.serial_number=1+number_of_patine
        appointment_obj.save()

        return HttpResponseRedirect(reverse('patient_app:appointment_history'))

@login_required
def confirmOnlineAppointment(request,doctor,appointment):
    doctor_obj=User.objects.get(id=doctor)

    appointments=get_object_or_404(OnlineAppointment,id=appointment)
    appointment_obj_find=OnlineDoctorAppointment.objects.filter(online_patient_d=request.user,online_doctor_d=doctor_obj,online_appointment_d=appointments,online_appointment_status=False)
    number_of_patinent=OnlineDoctorAppointment.objects.filter(online_patient_d=request.user,online_doctor_d=doctor_obj,online_appointment_d=appointments,online_appointment_status=False).count()
    
   
    if(number_of_patinent>=appointments.online_number_of_patient):
        messages.warning(request,'This slot already booked try another slot')
        return HttpResponseRedirect(reverse('patient_app:find_doctor'))

    elif(appointment_obj_find.exists()):
        messages.warning(request,"You have already appointment on this slot")
        url='/patient/make_appointmnet/{doctor_id}/'.format(doctor_id=doctor)
        return redirect(url)

    else:
        appointment_obj=OnlineDoctorAppointment.objects.get_or_create(online_patient_d=request.user,online_doctor_d=doctor_obj,online_appointment_d=appointments)
        appointment_obj=appointment_obj[0]
        appointment_obj.online_serial_number=1+number_of_patinent
        appointment_obj.save()

        return HttpResponseRedirect(reverse('patient_app:appointment_history'))

@login_required
def appointmentHistory(request):
    data_dic={}
    
    appointment_list_pending=DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=False).order_by('-id')

    if DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=False).exists():
        last_appointment=DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=False).latest('appointment_d')
        data_dic.update({'last_appointment':last_appointment,})

    online_appointment_list=OnlineDoctorAppointment.objects.filter(online_patient_d=request.user,online_appointment_status=False).order_by('-id')
    
        

    data_dic.update({'title':'Appointment History','appointment_list_pending':appointment_list_pending,'online_appointment_list':online_appointment_list})
    
    return render(request,'patient_app/appointmentHistory.html',context=data_dic)


def appointmentDetails(request,pk):
    details=DoctorAppointment.objects.get(id=pk)

    
    data_dic={'title':'Appointment Details','details':details,}
    return render(request,'patient_app/appointDetails.html',context=data_dic)

def onlineAppointmentDetails(request,pk):
    data_dic={'title':'Appointment Details'}

    details=OnlineDoctorAppointment.objects.get(id=pk)
    data_dic.update({'details':details})

    if PaymentStatus.objects.filter(payment_user=request.user,payment_appointment=details,payment_status=True).exists():

        payment=PaymentStatus.objects.get(payment_user=request.user,payment_appointment=details,payment_status=True)
        data_dic.update({'payment':payment})

    return render(request,'patient_app/onlineAppointDetails.html',context=data_dic)

def conformPayment(request,pk):
    payment=OnlineDoctorAppointment.objects.get(id=pk)
    data_dic={'title':'Confirm Payment'}

    form=PaymentStatusForm()
    data_dic.update({'form':form})

    if request.method=='POST':
        form=PaymentStatusForm(request.POST)
        form.instance.payment_user=request.user
        form.instance.payment_appointment=payment
        form.save()
        if form.is_valid():
            form.save()
            url='/payments/payment/{pk}/'.format(pk=pk)
            return redirect(url)

    return render(request,'patient_app/confirmPayment.html',context=data_dic)


def recentPrescription(request):
    data_dic={'title':'Recent Priscription'}
    patient_info=PatientInfo.objects.filter(user=request.user)
    patient_info=patient_info[0]

    #Prescription leatest
    if DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=True).exists():
        appointment_obj=DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=True).latest('doctor_d')
        prescription=Prescription.objects.filter(prescription_for=appointment_obj)
        doctor_details=prescription[0]

        next_meeting=Symptoms.objects.filter(symptoms_for=appointment_obj)[0]

        symptoms=Symptoms.objects.filter(symptoms_for=appointment_obj)[0]

        report_list=Reports.objects.filter(report_for=appointment_obj)

        report_file=ReportFile.objects.filter(file_for=appointment_obj)

        
        data_dic.update({'medicine_list':prescription,'doctor_details':doctor_details,'next_meeting':next_meeting,'symptom':symptoms,'reports_list':report_list,'report_file':report_file})
       
        

    data_dic.update({'patient_info':patient_info,})

    return render(request,'patient_app/prescription.html',context=data_dic)

def prescriptionList(request):
    data_dic={'title':'prescription'}

    #Prescription leatest
    if DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=True).exists():
        appointment_obj=DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=True).order_by('-id')
        data_dic.update({'prescription_list':appointment_obj})
        print("prescription List",appointment_obj)

    return render(request,'patient_app/prescriptionList.html',context=data_dic)

def onlinePrescriptionList(request):
    data_dic={'title':'prescription'}

   
    if OnlineDoctorAppointment.objects.filter(online_patient_d=request.user,online_appointment_status=True).exists():
        appointment_obj=OnlineDoctorAppointment.objects.filter(online_patient_d=request.user,online_appointment_status=True).order_by('-id')
        data_dic.update({'prescription_list':appointment_obj})
        print("prescription List",appointment_obj)

    return render(request,'patient_app/onlinePrescriptionList.html',context=data_dic)

def prescriptionDetails(request,pk):
    data_dic={'title':'prescripction Details'}

    patient_info=PatientInfo.objects.filter(user=request.user)
    patient_info=patient_info[0]

    data_dic.update({'patient_info':patient_info})


    if DoctorAppointment.objects.filter(patient_d=request.user,appointment_status=True).exists():
        appointment_obj=DoctorAppointment.objects.get(patient_d=request.user,id=pk,appointment_status=True)
        prescription=Prescription.objects.filter(prescription_for=appointment_obj)

        prescription=Prescription.objects.filter(prescription_for=appointment_obj)
        doctor_details=prescription[0]

        next_meeting=Symptoms.objects.filter(symptoms_for=appointment_obj)[0]

        symptoms=Symptoms.objects.filter(symptoms_for=appointment_obj)[0]

        report_list=Reports.objects.filter(report_for=appointment_obj)

        report_file=ReportFile.objects.filter(file_for=appointment_obj)
        data_dic.update({'report_file':report_file})
        
        
        data_dic.update({'medicine_list':prescription,'doctor_details':doctor_details,'next_meeting':next_meeting,'symptom':symptoms,'reports_list':report_list})

    return render(request,'patient_app/prescriptionDetails.html',context=data_dic)

def onlinePrescriptionDetails(request,pk):
    data_dic={'title':'prescripction Details'}

    patient_info=PatientInfo.objects.filter(user=request.user)
    patient_info=patient_info[0]

    data_dic.update({'patient_info':patient_info})


    if OnlineDoctorAppointment.objects.filter(online_patient_d=request.user,online_appointment_status=True).exists():
        appointment_obj=OnlineDoctorAppointment.objects.get(online_patient_d=request.user,id=pk,online_appointment_status=True)
        prescription=OnlinePrescription.objects.filter(Online_prescription_for=appointment_obj)

        if OnlinePrescription.objects.filter(Online_prescription_for=appointment_obj).exists():
            prescription=OnlinePrescription.objects.filter(Online_prescription_for=appointment_obj)
            doctor_details=prescription[0]
            data_dic.update( {'doctor_details':doctor_details} )

        next_meeting=OnlineSymptoms.objects.filter(online_symptoms_for=appointment_obj)[0]

        symptoms=OnlineSymptoms.objects.filter(online_symptoms_for=appointment_obj)[0]

        report_list=OnlineReports.objects.filter(online_report_for=appointment_obj)

        report_file=OnlineReportFile.objects.filter(online_file_for=appointment_obj)
        data_dic.update({'report_file':report_file})
        
        
        data_dic.update({'medicine_list':prescription,'next_meeting':next_meeting,'symptom':symptoms,'reports_list':report_list})

    return render(request,'patient_app/onlinePrescriptionDetails.html',context=data_dic)
