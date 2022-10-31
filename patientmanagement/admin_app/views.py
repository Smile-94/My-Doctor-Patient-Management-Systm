
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from datetime import date


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

from django.contrib.auth.models import Group
from django.conf import settings

#Forms and model
from login_app.models import Profile
from login_app.models import User
from login_app.forms import profileForm
from login_app.forms import signUpForm
from doctor_app.models import Appointment
from doctor_app.models import OnlineAppointment
from appointment_app.models import DoctorAppointment
from appointment_app.models import OnlineDoctorAppointment
from doctor_app.models import DoctorInfo
from prescription_app.models import Prescription
from prescription_app.models import Symptoms
from prescription_app.models import Reports
from prescription_app.models import ReportFile
from prescription_app.models import OnlinePrescription
from prescription_app.models import OnlineReports
from prescription_app.models import OnlineReportFile
from prescription_app.models import OnlineSymptoms
from prescription_app.forms import ReportFileForm
from prescription_app.forms import OnlinePrescriptionForm
from prescription_app.forms import OnlineReportsForm
from prescription_app.forms import OnlineReportFileForm




#admin app forms & model
from admin_app.models import DoctorCatagory
from admin_app.forms import DoctorCatagoryForm
#messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# class based view
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

#for Dashboard
from django.db.models import Count

# Create your views here.

# Admin dashboard view function
@login_required
def adminDashboard(request):
    #Total patient
    total_patient=Profile.objects.filter(user_catagory='PATIENT').count()

    #total Doctor
    total_doctor=Profile.objects.filter(user_catagory='DOCTOR').count()
    doctor_pending=Profile.objects.filter(user_catagory='DOCTOR',status=False)
    user=User.objects.all()

    #total requested doctor
    total_doctor_pending=Profile.objects.filter(user_catagory='DOCTOR',status=False).count()

    todays_patient_count=0
    if Appointment.objects.filter(appointment_date=date.today()).exists():
        todays_object=Appointment.objects.filter(appointment_date=date.today())

        todays_patient_count=0
        for patient in todays_object:
            todays_patient_count +=DoctorAppointment.objects.filter(appointment_d=patient).count()

    doctor_catagory=DoctorCatagory.objects.all().order_by('doctor_catagoy')
    
    data_dic={
        'title':'Admin Dashboard',
        'total_patient':total_patient,
        'total_doctor':total_doctor,
        'doctor_pending':doctor_pending,
        'total_doctor_pending':total_doctor_pending,
        'todays_patient':todays_patient_count,
        'doctor_catagory':doctor_catagory,
        'users':'user'
        }
    return render(request,'admin_app/adminMain.html',context=data_dic)


# Patient List function
@login_required
def patientList(request):
    patinent_list=Profile.objects.filter(user_catagory='PATIENT')
    data_dic={'title':'Patient List','patient_list':patinent_list}
    return render(request,'admin_app/patientList.html',context=data_dic)

#Doctor Details function
@method_decorator(login_required,name='dispatch')
class doctorDetail(DetailView):
    model = User
    context_object_name='doctor_details'
    template_name = 'admin_app/doctorDetails.html'
    success_url=reverse_lazy('admin_app:admin_dash')
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Doctor Details'
        context['pending']=Profile.objects.filter(status=False,user_catagory='DOCTOR')

        return context
@login_required
def doctorRequest(request):
    data_dic={'title':'Doctor Request'}

    doctor_pending=Profile.objects.filter(user_catagory='DOCTOR',status=False)
    data_dic.update({'doctor_pending':doctor_pending})

    return render(request,'admin_app/doctorRequest.html',context=data_dic)


@login_required
def addDoctor(request,pk):
    doctor=Profile.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    messages.success(request,'Doctor hasbeen added successfully')
    return HttpResponseRedirect(reverse('admin_app:admin_dash'))

@login_required
def doctorList(request):
    doctor_list=Profile.objects.filter(user_catagory='DOCTOR')
    user=User.objects.filter(groups=2)
    data_dic={'title':'Doctor List','doctor_list':doctor_list}
    return render(request,'admin_app/doctorList.html',context=data_dic)

@method_decorator(login_required,name='dispatch')
class editDoctor(UpdateView, SuccessMessageMixin):

    fields=('date_of_birth','national_ID_number','passport_number','registration_number_BMDC')

    model=DoctorInfo
    template_name='admin_app/editDoctor.html'
    success_url=reverse_lazy('admin_app:doctor_list')
    success_message = "Doctor profile updated successfully"



@login_required
def prescribedpatientList(request):
    data_dic={'title':'Patient List'}

    prescribed_patient=DoctorAppointment.objects.filter(appointment_status=True).order_by('-id')
    data_dic.update({'prescribed_patient':prescribed_patient})

    return render(request,'admin_app/prescribedPatientList.html',context=data_dic)

@login_required
def onlinePrescribedpatientList(request):
    data_dic={'title':'Patient List'}

    prescribed_patient=OnlineDoctorAppointment.objects.filter(online_appointment_status=True).order_by('-id')
    data_dic.update({'prescribed_patient':prescribed_patient})

    return render(request,'admin_app/onliePrescribePatientList.html',context=data_dic)

@login_required
def prescribedPatientDetails(request,pk):
    data_dic={'title':'Patient Details'}

    patient_details=DoctorAppointment.objects.get(id=pk,appointment_status=True)
    data_dic.update({'patient_details':patient_details})

    medicine_list=Prescription.objects.filter(prescription_for=patient_details)
    data_dic.update({'medicine_list':medicine_list})

    report_list=Reports.objects.filter(report_for=patient_details)
    data_dic.update({'report_list':report_list})

    report_file=ReportFile.objects.filter(file_for=patient_details)
    data_dic.update({'report_file':report_file})
    return render(request,'admin_app/prescribedPatientDetails.html',context=data_dic)

#Online Prescribed Patient Details
@login_required
def prescribedPatientDetails(request,pk):
    data_dic={'title':'Patient Details'}

    patient_details=OnlineDoctorAppointment.objects.get(id=pk,online_appointment_status=True)
    data_dic.update({'patient_details':patient_details})

    medicine_list=OnlinePrescription.objects.filter(Online_prescription_for=patient_details)
    data_dic.update({'medicine_list':medicine_list})

    report_list=OnlineReports.objects.filter(online_report_for=patient_details)
    data_dic.update({'report_list':report_list})

    report_file=OnlineReportFile.objects.filter(online_file_for=patient_details)
    data_dic.update({'report_file':report_file})
    return render(request,'admin_app/onlinePrescribedPatientDetails.html',context=data_dic)


@login_required
def patientWaitReport(request):
    data_dic={'title':'Wating for Report'}
    report_patient=DoctorAppointment.objects.filter(report_status=False,appointment_status=True)
    data_dic.update({'report_patient':report_patient})

    return render(request,'admin_app/waitReport.html',context=data_dic)

@login_required
def onlinePatientWaitReport(request):
    data_dic={'title':'Wating for Report'}
    report_patient=OnlineDoctorAppointment.objects.filter(online_report_status=False,online_appointment_status=True)
    data_dic.update({'report_patient':report_patient})

    return render(request,'admin_app/onlineWaitReport.html',context=data_dic)

@login_required
def submitReport(request,pk):
    data_dic={'title':'Submit Report'}

    report_patient=DoctorAppointment.objects.get(id=pk)
    test_report=Reports.objects.filter(report_for=report_patient)
    data_dic.update({'test_report':test_report})

    form=ReportFileForm()
    data_dic.update({'form':form})

    if request.method=='POST':
        form=ReportFileForm(request.POST,request.FILES)
        form.instance.file_for=report_patient
        print()
        form.save()
        if form.is_valid():
            form.save()
            report_patient.report_status=True
            report_patient.save()
            messages.success(request,'Added Report file successfully')

    report_file=ReportFile.objects.filter(file_for=report_patient) 
    data_dic.update({'report_file':report_file})

    return render(request,'admin_app/submitReportForm.html',context=data_dic)

#Online Submit Pathology Report Function
@login_required
def OnlineSubmitReport(request,pk):
    data_dic={'title':'Submit Report'}

    report_patient=OnlineDoctorAppointment.objects.get(id=pk)
    test_report=OnlineReports.objects.filter(online_report_for=report_patient)
    data_dic.update({'test_report':test_report})

    form=OnlineReportFileForm()
    data_dic.update({'form':form})

    if request.method=='POST':
        form=OnlineReportFileForm(request.POST,request.FILES)
        form.instance.online_file_for=report_patient
        print()
        form.save()
        if form.is_valid():
            form.save()
            report_patient.online_report_status=True
            report_patient.save()
            messages.success(request,'Added Report file successfully')

    report_file=OnlineReportFile.objects.filter(online_file_for=report_patient) 
    data_dic.update({'report_file':report_file})

    return render(request,'admin_app/submitOnlineReportForm.html',context=data_dic)

@login_required
def todaysAppointmentList(request):
    data_dic={'title':'Appointment List'}
    todays_appointment=Appointment.objects.filter(appointment_date=date.today(),active_status='ACTIVE',cancel_status=False)
    data_dic.update({'todays_appointment':todays_appointment})

    return render(request,'admin_app/todaysAppointList.html',context=data_dic)

@login_required
def allAppointmentList(request):
    data_dic={'title':'Appointment List'}
    all_appointment=Appointment.objects.filter(active_status='ACTIVE',cancel_status=False)
    data_dic.update({'all_appointment':all_appointment})

    return render(request,'admin_app/allAppointmentList.html',context=data_dic)

@login_required
def addDoctorCatagory(request):
    catagories=DoctorCatagory.objects.order_by('doctor_catagoy')
    form=DoctorCatagoryForm()
    data_dic={'title':'Doctor Catagoy','form':form,'catagories':catagories}

    if request.method=='POST':
        form=DoctorCatagoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Docotr Catagory Added Successfully')
            return HttpResponseRedirect(reverse('admin_app:add_catagory'))

    return render(request,'admin_app/addCatagory.html',context=data_dic)

@method_decorator(login_required,name='dispatch')
class updateCatagory(SuccessMessageMixin, UpdateView):
    fields=('doctor_catagoy',)
  
    model=DoctorCatagory
    template_name='admin_app/addCatagory.html'
    success_url=reverse_lazy('admin_app:add_catagory')
    success_message = "Catagory updated successfully"
    
@method_decorator(login_required,name='dispatch')
class deleteCatagory(SuccessMessageMixin, DeleteView):
    context_object_name='catagory'
    model=DoctorCatagory
    success_message = "Catagory deleted successfully"
    success_url=reverse_lazy('admin_app:add_catagory')
    template_name='admin_app/delete.html'

@login_required
def addUserRequest(request):
    data_dic={'title':'User Request'}

    request_user=Profile.objects.filter(user_catagory='ADMIN',status=False)
    data_dic.update({'request_user':request_user})
    return render(request,'admin_app/addUser.html',context=data_dic)

@login_required
def addUser(request,pk):
    data_dic={'title':'Add User'}
    
    user_request=Profile.objects.get(id=pk)
    user_request.status=True
    user_request.save()
    return HttpResponseRedirect(reverse('admin_app:user_request'))

@login_required
def doctorReport(request):
    data_dic={'title':'Doctor Report'}

    doctor_list=Profile.objects.filter(user_catagory='DOCTOR')
    data_dic.update({'doctor_list':doctor_list})

    return render(request,'admin_app/doctorReport.html',context=data_dic)
    
#Function for Doector Appointment and Prescription details 
@login_required
def doctorReportDetails(request,pk):
    data_dic={'title':'Report Details'}

    fromDate=date.today()
    toDate=date.today()

    user=User.objects.get(id=pk)

    total_offline_appointment=0
    total_online_appointment=0
    total_cancel_offline_appointment=0
    total_cancel_online_appointment=0

    total_offline_morning_appointmnet=0
    total_offline_afternoon_appointmnet=0
    total_offline_evening_appointmnet=0
    
    total_online_morning_appointment=0
    total_online_afternoon_appointment=0
    total_online_evening_appointment=0

    total_offline_prescription=DoctorAppointment.objects.filter(doctor_d=user).count()
    total_offline_notPrescribed=DoctorAppointment.objects.filter(doctor_d=user,appointment_status=False).count()

    total_online_prescription=OnlineDoctorAppointment.objects.filter(online_doctor_d=user).count()
    total_online_notprescribed=OnlineDoctorAppointment.objects.filter(online_doctor_d=user,online_appointment_status=False).count()

    total_offline_morning_prescription=0
    total_offline_afternoon_prescription=0
    total_offline_evening_prescription=0

    total_online_morning_prescription=0
    total_online_afternoon_prescription=0
    total_online_evening_prescription=0

    if Appointment.objects.filter(appoint_user=user,).exists():
        all_appointment=Appointment.objects.filter(appoint_user=user)
        total_offline_appointment=Appointment.objects.filter(appoint_user=user).count()

        total_cancel_offline_appointment=Appointment.objects.filter(appoint_user=user,cancel_status=True).count()

        total_offline_morning_appointmnet=Appointment.objects.filter(appoint_user=user,time_slot='Morning(9.00am-1.00pm)',cancel_status=False).count()
        total_offline_afternoon_appointmnet=Appointment.objects.filter(appoint_user=user,time_slot='Afternoon(4.00pm-6.30pm)',cancel_status=False).count()
        total_offline_evening_appointmnet=Appointment.objects.filter(appoint_user=user,time_slot='Evening(7.30pm-8.30pm)',cancel_status=False).count()

        if Appointment.objects.filter(appoint_user=user,time_slot='Morning(9.00am-1.00pm)').exists():
            offline_morning_appointmnet=Appointment.objects.filter(appoint_user=user,time_slot='Morning(9.00am-1.00pm)')[0]
            total_offline_morning_prescription=DoctorAppointment.objects.filter(appointment_d=offline_morning_appointmnet,appointment_status=True).count()

        if Appointment.objects.filter(appoint_user=user,time_slot='Afternoon(4.00pm-6.30pm)').exists():
            toffline_afternoon_appointmnet=Appointment.objects.filter(appoint_user=user,time_slot='Afternoon(4.00pm-6.30pm)')[0]
            total_offline_afternoon_prescription=DoctorAppointment.objects.filter(appointment_d=toffline_afternoon_appointmnet,appointment_status=True).count()

        if Appointment.objects.filter(appoint_user=user,time_slot='Evening(7.30pm-8.30pm)').exists():
            offline_evening_appointmnet=Appointment.objects.filter(appoint_user=user,time_slot='Evening(7.30pm-8.30pm)')[0]
            total_offline_evening_prescription=DoctorAppointment.objects.filter(appointment_d=offline_evening_appointmnet,appointment_status=True).count()
        

    if OnlineAppointment.objects.filter(appointment_user=user).exists():
        all_online_appointment=OnlineAppointment.objects.filter(appointment_user=user)

        total_online_appointment=OnlineAppointment.objects.filter(appointment_user=user).count()

        total_cancel_online_appointment=OnlineAppointment.objects.filter(appointment_user=user,online_cancel_status=True).count()

        total_online_morning_appointment=OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Morning(9.00am-1.00pm)',online_cancel_status=False).count()
        total_online_afternoon_appointment=OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Afternoon(4.00pm-6.30pm)',online_cancel_status=False).count()
        total_online_evening_appointment=OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Evening(7.30pm-8.30pm)',online_cancel_status=False).count()

        if OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Morning(9.00am-1.00pm)').exists():
            online_morning_appointment=OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Morning(9.00am-1.00pm)')[0]
            total_online_morning_prescription=OnlineDoctorAppointment.objects.filter(online_appointment_d=online_morning_appointment,online_appointment_status=True).count()

        if OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Morning(9.00am-1.00pm)').exists():
            online_afternoon_appointment=OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Morning(9.00am-1.00pm)')[0]
            total_online_afternoon_prescription=OnlineDoctorAppointment.objects.filter(online_appointment_d=online_afternoon_appointment,online_appointment_status=True).count()

        if OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Evening(7.30pm-8.30pm)').exists():
            online_evening_appointment=OnlineAppointment.objects.filter(appointment_user=user,online_time_slot='Evening(7.30pm-8.30pm)')[0]
            total_online_evening_prescription=OnlineDoctorAppointment.objects.filter(online_appointment_d=online_evening_appointment,online_appointment_status=True).count()


        
    total_appointment=(total_offline_appointment+total_online_appointment)
    total_appointment_cancel=(total_cancel_offline_appointment+total_cancel_online_appointment)

    total_morning_appointment=(total_offline_morning_appointmnet+total_online_morning_appointment)
    total_afternoon_appointment=(total_offline_afternoon_appointmnet+total_online_afternoon_appointment)
    total_evening_appointment=(total_offline_evening_appointmnet+total_online_evening_appointment)

    #Percentage Appointment
    morning_percentage=0.0
    afternoon_percentage=0.0
    evening_percentage=0.0
    cancel_percentage=0.0

    if total_appointment !=0:
        morning_percentage=((total_morning_appointment/total_appointment)*100)
        afternoon_percentage=((total_afternoon_appointment/total_appointment)*100)
        evening_percentage=((total_evening_appointment/total_appointment)*100)
        cancel_percentage=((total_appointment_cancel/total_appointment)*100)

    offline_morning_percentage=0.0
    offline_afternoon_percentage=0.0
    offline_evening_percentage=0.0
    offline_cancel_percentage=0.0


    if total_offline_appointment !=0:
        offline_morning_percentage=((total_offline_morning_appointmnet/total_offline_appointment)*100)
        offline_afternoon_percentage=((total_offline_afternoon_appointmnet/total_offline_appointment)*100)
        offline_evening_percentage=((total_offline_evening_appointmnet/total_offline_appointment)*100)
        offline_cancel_percentage=((total_cancel_offline_appointment/total_offline_appointment)*100)
    
    online_morning_percentage=0.0
    online_afternoon_percentage=0.0
    online_evening_percentage=0.0
    online_cancel_percentage=0.0

    if total_online_appointment !=0:
        online_morning_percentage=((total_online_morning_appointment/total_online_appointment)*100)
        online_afternoon_percentage=((total_online_afternoon_appointment/total_online_appointment)*100)
        online_evening_percentage=((total_online_evening_appointment/total_online_appointment)*100)
        online_cancel_percentage=((total_cancel_online_appointment/total_online_appointment)*100)

    #Percentage Prescription
    offline_morning_pres_percen=0.0
    offline_afternoon_pres_percen=0.0
    offline_evening_pres_percen=0.0
    offline_not_pres_percen=0.0

    if total_offline_prescription !=0:
        offline_morning_pres_percen=((total_offline_morning_prescription/total_offline_prescription)*100)
        offline_afternoon_pres_percen=((total_offline_afternoon_prescription/total_offline_prescription)*100)
        offline_evening_pres_percen=((total_offline_evening_prescription/total_offline_prescription)*100)
        offline_not_pres_percen=((total_offline_notPrescribed/total_offline_prescription)*100)
    


    online_morning_pres_percent=0.0
    online_afternoon_pres_percent=0.0
    online_evening_pres_percent=0.0
    online_not_pres_percent=0.0

    if total_online_prescription !=0:
        online_morning_pres_percent=((total_online_morning_prescription/total_online_prescription)*100)
        online_afternoon_pres_percent=((total_online_morning_prescription/total_online_prescription)*100)
        online_evening_pres_percent=((total_online_morning_prescription/total_online_prescription)*100)
        online_not_pres_percent=((total_online_notprescribed/total_online_prescription)*100)




    data_dic.update({
        'fromDate':fromDate,
        'toDate':toDate,
        'doctor':user,
        'total_appointment':total_appointment,
        'total_offline_appointment':total_offline_appointment,
        'total_online_appointment':total_online_appointment,
        'total_appointment_cancel':total_appointment_cancel,
        'total_cancel_offline_appointment':total_cancel_offline_appointment,
        'total_cancel_online_appointment':total_cancel_online_appointment,

        'total_morning_appointment':total_morning_appointment,
        'total_afternoon_appointment':total_afternoon_appointment,
        'total_evening_appointment':total_evening_appointment,

        'total_offline_morning_appointment':total_offline_morning_appointmnet,
        'total_offline_afternoon_appointmnet':total_offline_afternoon_appointmnet,
        'total_offline_evening_appointmnet':total_offline_evening_appointmnet,

        'total_online_morning_appointment':total_online_morning_appointment,
        'total_online_afternoon_appointment':total_online_afternoon_appointment,
        'total_online_evening_appointment':total_online_evening_appointment,

        'total_offline_prescription':total_offline_prescription,
        'total_offline_morning_prescription':total_offline_morning_prescription,
        'total_offline_afternoon_prescription':total_offline_afternoon_prescription,
        'total_offline_evening_prescription':total_offline_evening_prescription,
        'total_offline_notPrescribed':total_offline_notPrescribed,

        'total_online_prescription':total_online_prescription,
        'total_online_morning_prescription':total_online_morning_prescription,
        'total_online_afternoon_prescription':total_online_afternoon_prescription,
        'total_online_evening_prescription':total_online_evening_prescription,
        'total_online_notprescribed':total_online_notprescribed,

        'morning_percentage':morning_percentage,
        'afternoon_percentage':afternoon_percentage,
        'evening_percentage':evening_percentage,
        'cancel_percentage':cancel_percentage,

        'offline_morning_percentage':offline_morning_percentage,
        'offline_afternoon_percentage':offline_afternoon_percentage,
        'offline_evening_percentage':offline_evening_percentage,
        'offline_cancel_percentage':offline_cancel_percentage,

        'online_morning_percentage':online_morning_percentage,
        'online_afternoon_percentage':online_afternoon_percentage,
        'online_evening_percentage':online_evening_percentage,
        'online_cancel_percentage':online_cancel_percentage,


        'offline_morning_pres_percen':offline_morning_pres_percen,
        'offline_afternoon_pres_percen':offline_afternoon_pres_percen,
        'offline_evening_pres_percen':offline_evening_pres_percen,
        'offline_not_pres_percen':offline_not_pres_percen,

        'online_morning_pres_percent':online_morning_pres_percent,
        'online_afternoon_pres_percent':online_afternoon_pres_percent,
        'online_evening_pres_percent':online_evening_pres_percent,
        'online_not_pres_percent':online_not_pres_percent,



    })
   

    return render(request,'admin_app/doctorReportDetails.html',context=data_dic)


def searchFromTo(request,pk):
    data_dic={'title':'Doctor Report'}
    doctor=Profile.objects.get(id=pk)
    data_dic.update({'doctor':doctor})
    


    if request.method=='POST':
        from_date=request.POST.get('fromDate')
        to_date=request.POST.get('toDate')

    total_offline_appointment=0    
    total_online_appointment=0 

    total_offline_morning_appointment=0
    total_offline_afternoon_appointment=0
    total_offline_evening_appointment=0
    total_offline_cancel_appointment=0
    

    

    total_offline_prescription=0
    total_offline_morning_prescription=0
    total_offline_afternoon_prescription=0
    total_offline_evening_prescription=0
    total_offline_not_prescribed=0

    offline_morning_not_prescribed=0
    offline_afternoon_not_prescribed=0
    offline_evening_not_prescribed=0

    
    offline_appointment=[]

    offline_doctor_prescription=[]
    offline_doctor_not_prescribed=[]

    if Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date).exists():
        offline_appointment.extend(list(Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date))) 
        offline_morning_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date,time_slot='Morning(9.00am-1.00am)',cancel_status=False)
        offline_afternoon_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date,time_slot='Afternoon(4.00pm-6.30pm)',cancel_status=False)
        offline_evening_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date,time_slot='Evening(7.30pm-8.30pm)',cancel_status=False)


        total_offline_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date).count()
        total_offline_morning_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date,time_slot='Morning(9.00am-1.00am)',cancel_status=False).count()
        total_offline_afternoon_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date,time_slot='Afternoon(4.00pm-6.30pm)',cancel_status=False).count()
        total_offline_evening_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date,time_slot='Evening(7.30pm-8.30pm)',cancel_status=False).count()
        total_offline_cancel_appointment=Appointment.objects.filter(appoint_user=pk,appointment_date__lte=to_date,appointment_date__gte=from_date,cancel_status=True).count()
        

        
        for appointment in offline_appointment:
            offline_doctor_prescription.extend(list(DoctorAppointment.objects.filter(appointment_d=appointment)))
            total_offline_prescription += DoctorAppointment.objects.filter(appointment_d=appointment)

        for appointment in offline_appointment:
            total_offline_not_prescribed=DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=False).count()
            offline_doctor_not_prescribed.extend(list(DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=False)))
            

        for appointment in offline_morning_appointment:
            total_offline_morning_prescription +=DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=True).count()
            offline_morning_not_prescribed +=DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=False).count()

        for appointment in offline_afternoon_appointment:
            total_offline_afternoon_prescription +=DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=True).count()
            offline_afternoon_not_prescribed +=DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=False).count()

        for appointment in offline_evening_appointment:
            total_offline_evening_prescription +=DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=True).count()
            offline_evening_not_prescribed +=DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=False).count()
        
        
            

    total_online_morning_appointment=0
    total_online_afternoon_appointment=0
    total_online_evening_appointment=0
    total_online_cancel_appointment=0 


    total_online_prescription=0
    total_online_morning_prescription=0
    total_online_afternoon_prescription=0
    total_online_evening_prescription=0
    total_online_not_prescribed=0

    online_morning_not_prescribed=0
    online_afternoon_not_prescribed=0
    online_evening_not_prescribed=0

    online_doctor_prescription=[]
    online_doctor_not_prescribed=[]
    
    if OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date).exists():
        online_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date)
        data_dic.update({'online_appointment':online_appointment})

        online_morning_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date,online_time_slot='Morning(9.00am-1.00pm)',online_cancel_status=False)
        online_evening_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date,online_time_slot='Afternoon(4.00pm-6.30pm)',online_cancel_status=False)
        online_afternoon_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date,online_time_slot='Evening(7.30pm-8.30pm)',online_cancel_status=False)

        total_online_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date).count()
        total_online_morning_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date,online_time_slot='Morning(9.00am-1.00pm)',online_cancel_status=False).count()
        total_online_afternoon_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date,online_time_slot='Afternoon(4.00pm-6.30pm)',online_cancel_status=False).count()
        total_online_evening_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date,online_time_slot='Evening(7.30pm-8.30pm)',online_cancel_status=False).count()
        total_online_cancel_appointment=OnlineAppointment.objects.filter(appointment_user=pk,online_appointment_date__lte=to_date,online_appointment_date__gte=from_date,online_cancel_status=True).count()


        
        for appointment in online_appointment:
            online_doctor_prescription.extend(list(OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment)))
            total_online_prescription +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment).count()
            total_online_not_prescribed +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=False).count()
            online_doctor_not_prescribed.extend(list(OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=False)))


        for appointment in online_morning_appointment:
            total_online_morning_prescription +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=True).count()
            online_morning_not_prescribed +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=False).count()

        for appointment in online_afternoon_appointment:
            total_online_afternoon_prescription +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=True).count()
            online_afternoon_not_prescribed +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=False).count()

        for appointment in online_evening_appointment:
            total_online_evening_prescription +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=True).count()
            online_evening_not_prescribed +=OnlineDoctorAppointment.objects.filter(online_appointment_d=appointment,online_appointment_status=False).count()
        

        


    total_appointment=(total_offline_appointment+total_online_appointment)
    total_morning_appointment=(total_offline_morning_appointment+total_online_morning_appointment)
    total_afternoon_appointment=(total_offline_afternoon_appointment+total_online_afternoon_appointment)
    total_evening_appointment=(total_offline_evening_appointment+total_online_evening_appointment)
    total_cancel_appointment=(total_offline_cancel_appointment+total_online_cancel_appointment)


    #Offline Percentage
    morning_percentage=0.0
    afternoon_percentage=0.0
    evening_percentage=0.0
    cancel_percentage=0.0

    if total_appointment !=0:
        morning_percentage=((total_morning_appointment/total_appointment)*100)
        afternoon_percentage=((total_afternoon_appointment/total_appointment)*100)
        evening_percentage=((total_evening_appointment/total_appointment)*100)
        cancel_percentage=((total_cancel_appointment/total_appointment)*100)


    offline_appoin_morning_percentage=0.0
    offline_appoin_afternoon_percentage=0.0
    offline_appoin_evening_percentage=0.0
    offline_appoin_cancel_percentage=0.0

    if total_offline_appointment !=0:
        offline_appoin_morning_percentage=((total_offline_morning_appointment/total_offline_appointment)*100)
        offline_appoin_afternoon_percentage=((total_offline_afternoon_appointment/total_offline_appointment)*100)
        offline_appoin_evening_percentage=((total_offline_evening_appointment/total_offline_appointment)*100)
        offline_appoin_cancel_percentage=((total_offline_cancel_appointment/total_offline_appointment)*100)

    #Online appointment percentage
    online_appoin_morning_percentage=0.0
    online_appoin_afternoon_percentage=0.0
    online_appoin_evening_percentage=0.0
    online_appoin_cancel_percentage=0.0

    if total_online_appointment !=0:
        online_appoin_morning_percentage=((total_online_morning_appointment/total_online_appointment)*100)
        online_appoin_afternoon_percentage=((total_online_afternoon_appointment/total_online_appointment)*100)
        online_appoin_evening_percentage=((total_online_evening_appointment/total_online_appointment)*100)
        online_appoin_cancel_percentage=((total_online_cancel_appointment/total_online_appointment)*100)
    
    #Offline Prescription
    offline_percentage_morning_prescription=0.0
    offline_percentage_afternoon_prescription=0.0
    offline_percentage_evening_prescription=0.0
    offline_percentage_not_prescription=0.0

    if total_offline_prescription !=0:
        offline_percentage_morning_prescription=((total_offline_morning_prescription/total_offline_prescription)*100)
        offline_percentage_afternoon_prescription=((total_offline_afternoon_prescription/total_offline_prescription)*100)
        offline_percentage_evening_prescription=((total_offline_evening_prescription/total_offline_prescription)*100)
        offline_percentage_not_prescription=((total_offline_not_prescribed/total_offline_prescription)*100)

    #Online Prescription
    online_percentage_morning_prescription=0.0
    online_percentage_afternoon_prescription=0.0
    online_percentage_evening_prescription=0.0
    online_percentage_not_prescription=0.0

    if total_online_prescription !=0:
        online_percentage_morning_prescription=((total_online_morning_prescription/total_online_prescription)*100)
        online_percentage_afternoon_prescription=((total_online_afternoon_prescription/total_online_prescription)*100)
        online_percentage_evening_prescription=((total_online_evening_prescription/total_online_prescription)*100)
        online_percentage_not_prescription=((total_online_not_prescribed/total_online_prescription)*100)

    #offline not prescribed percentage
    offline_morning_not_pres_percentage=0.0
    offline_afternoon_not_pres_percentage=0.0
    offline_evening_not_pres_percentage=0.0

    if total_offline_not_prescribed !=0:
        offline_morning_not_pres_percentage=((offline_morning_not_prescribed/total_offline_not_prescribed)*100)
        offline_afternoon_not_pres_percentage=((offline_afternoon_not_prescribed/total_offline_not_prescribed)*100)
        offline_evening_not_pres_percentage=((offline_evening_not_prescribed/total_offline_not_prescribed)*100)


    #Online not prescribed percentage
    online_morning_not_pres_percentage=0.0
    online_afternoon_not_pres_percentage=0.0
    online_evening_not_pres_percentage=0.0

    if total_online_not_prescribed !=0:
        online_morning_not_pres_percentage=((online_morning_not_prescribed/total_online_not_prescribed)*100)
        online_afternoon_not_pres_percentage=((online_afternoon_not_prescribed/total_online_not_prescribed)*100)
        online_evening_not_pres_percentage=((online_evening_not_prescribed/total_online_not_prescribed)*100)


    data_dic.update({
        'pk':pk,

        'from_date':from_date,
        'to_date':to_date,

        'offline_appointment':offline_appointment,
        'offline_doctor_prescription':offline_doctor_prescription,
        'online_doctor_prescription':online_doctor_prescription,
        'offline_doctor_not_prescribed':offline_doctor_not_prescribed,
        'online_doctor_not_prescribed':online_doctor_not_prescribed,

        'total_appointment':total_appointment,
        'total_morning_appointment':total_morning_appointment,
        'total_afternoon_appointment':total_afternoon_appointment,
        'total_evening_appointment':total_evening_appointment,
        'total_cancel_appointment':total_cancel_appointment,


        'total_offline_appointment':total_offline_appointment,
        'total_offline_morning_appointment':total_offline_morning_appointment,
        'total_offline_afternoon_appointment':total_offline_afternoon_appointment,
        'total_offline_evening_appointment':total_offline_evening_appointment,
        'total_offline_cancel_appointment':total_offline_cancel_appointment,

        'total_online_appointment':total_online_appointment,
        'total_online_morning_appointment':total_online_morning_appointment,
        'total_online_afternoon_appointment':total_online_afternoon_appointment,
        'total_online_evening_appointment':total_online_evening_appointment,
        'total_online_cancel_appointment':total_online_cancel_appointment,

        'total_offline_prescription':total_offline_prescription,
        'total_offline_morning_prescription':total_offline_morning_prescription,
        'total_offline_afternoon_prescription':total_offline_morning_prescription,
        'total_offline_evening_prescription':total_offline_morning_prescription,
        'total_offline_not_prescribed':total_offline_not_prescribed,

        'total_online_prescription':total_online_prescription,
        'total_online_morning_prescription':total_online_morning_prescription,
        'total_online_afternoon_prescription':total_online_afternoon_prescription,
        'total_online_evening_prescription':total_online_evening_prescription,
        'total_online_not_prescribed':total_online_not_prescribed,

        'morning_percentage':morning_percentage,
        'afternoon_percentage':afternoon_percentage,
        'evening_percentage':evening_percentage,
        'cancel_percentage':cancel_percentage,

        'offline_appoin_morning_percentage':offline_appoin_morning_percentage,
        'offline_appoin_afternoon_percentage':offline_appoin_afternoon_percentage,
        'offline_appoin_evening_percentage':offline_appoin_evening_percentage,
        'offline_appoin_cancel_percentage':offline_appoin_cancel_percentage,

        'online_appoin_morning_percentage':online_appoin_morning_percentage,
        'online_appoin_afternoon_percentage':online_appoin_afternoon_percentage,
        'online_appoin_evening_percentage':online_appoin_evening_percentage,
        'online_appoin_cancel_percentage':online_appoin_cancel_percentage,

        'offline_percentage_morning_prescription':offline_percentage_morning_prescription,
        'offline_percentage_afternoon_prescription':offline_percentage_afternoon_prescription,
        'offline_percentage_evening_prescription':offline_percentage_evening_prescription,
        'offline_percentage_not_prescription':offline_percentage_not_prescription,

        'online_percentage_morning_prescription':online_percentage_morning_prescription,
        'online_percentage_afternoon_prescription':online_percentage_afternoon_prescription,
        'online_percentage_evening_prescription':online_percentage_evening_prescription,
        'online_percentage_not_prescription':online_percentage_not_prescription,

        'offline_morning_not_prescribed':offline_morning_not_prescribed,
        'offline_afternoon_not_prescribed':offline_afternoon_not_prescribed,
        'offline_evening_not_prescribed':offline_evening_not_prescribed,

        'online_morning_not_prescribed':online_morning_not_prescribed,
        'online_afternoon_not_prescribed':online_afternoon_not_prescribed,
        'online_evening_not_prescribed':online_evening_not_prescribed,

        'offline_morning_not_pres_percentage':offline_morning_not_pres_percentage,
        'offline_afternoon_not_pres_percentage':offline_afternoon_not_pres_percentage,
        'offline_evening_not_pres_percentage':offline_evening_not_pres_percentage,

        'online_morning_not_pres_percentage':online_morning_not_pres_percentage,
        'online_afternoon_not_pres_percentage':online_afternoon_not_pres_percentage,
        'online_evening_not_pres_percentage':online_evening_not_pres_percentage,


    })   
            
    # data_dic.update({'offline_appointment':offline_appointment,'online_appointment':online_appointment})

    return render(request,'admin_app/doctorFromToReport.html',context=data_dic)



@login_required
def doctorStatics(request):
    data_dic={'title':'Doctor Reports'}
    catagory=DoctorCatagory.objects.all().order_by('doctor_catagoy')
    data_dic.update({'catagories':catagory})


    number_of_doctor=[]
    for specilist in catagory:
        number_of_doctor.append(DoctorInfo.objects.filter(specialist=specilist).count())
 
    data_dic.update({'number_of_doctor':number_of_doctor})

   
    
    cancel_appointment=Appointment.objects.filter(cancel_status=True,appointment_date=date.today()).count()
    morning_appointment=Appointment.objects.filter(active_status='ACTIVE',appointment_date=date.today(),time_slot='Morning(9.00am-1.00pm)').count()
    afternoon_appointment=Appointment.objects.filter(active_status='ACTIVE',appointment_date=date.today(),time_slot='Afternoon(4.00pm-6.30pm)').count()
    evening_appointment=Appointment.objects.filter(active_status='ACTIVE',appointment_date=date.today(),time_slot='Evening(7.30pm-8.30pm)').count()

    data_dic.update({
        'morning_appointment':morning_appointment,
        'cancel_appointment':cancel_appointment,
        'afternoon_appointment':afternoon_appointment,
        'evening_appointment':evening_appointment})

    total_cancel_appointment=Appointment.objects.filter(cancel_status=True,).count()
    total_morning_appointment=Appointment.objects.filter(active_status='ACTIVE',time_slot='Morning(9.00am-1.00pm)').count()
    total_afternoon_appointment=Appointment.objects.filter(active_status='ACTIVE',time_slot='Afternoon(4.00pm-6.30pm)').count()
    total_evening_appointment=Appointment.objects.filter(active_status='ACTIVE',time_slot='Evening(7.30pm-8.30pm)').count()
    
    data_dic.update({
        'total_cancel_appointment':total_cancel_appointment,
        'total_morning_appointment': total_morning_appointment,
        'total_afternoon_appointment':total_afternoon_appointment,
        'total_evening_appointment':total_evening_appointment,
    })

    morning_appoint_percen=0.0
    afternoon_appoint_percen=0.0
    evening_appoint_percen=0.0
    cancel_appoint_percen=0.0

    total_appointment=Appointment.objects.count()
    if total_appointment !=0:
        morning_appoint_percen=((total_morning_appointment/total_appointment)*100)
        afternoon_appoint_percen=((total_afternoon_appointment/total_appointment)*100)
        evening_appoint_percen=((total_evening_appointment/total_appointment)*100)
        cancel_appoint_percen=((total_cancel_appointment/total_appointment)*100)

    data_dic.update({
        'morning_appoint_percen':morning_appoint_percen,
        'afternoon_appoint_percen':afternoon_appoint_percen,
        'evening_appoint_percen':evening_appoint_percen,
        'cancel_appoint_percen':cancel_appoint_percen,
    })
    

    return render(request,'admin_app/doctorStatics.html',context=data_dic,) 

@login_required
def patientStatics(request):
    data_dic={'title':'Patient Statics'}

    morning_appoint=Appointment.objects.filter(appointment_date=date.today(),time_slot='Morning(9.00am-1.00pm)',cancel_status=False)
    afternoon_appoint=Appointment.objects.filter(appointment_date=date.today(),time_slot='Afternoon(4.00pm-6.30pm)',cancel_status=False)
    evening_appoint=Appointment.objects.filter(appointment_date=date.today(),time_slot='Evening(7.30pm-8.30pm)',cancel_status=False)
    cancel_appoint=Appointment.objects.filter(appointment_date=date.today(),cancel_status=True)

    today_appoint=Appointment.objects.filter(appointment_date=date.today(),cancel_status=False)

    today_morning_patient=0
    for appoint in morning_appoint:
        today_morning_patient += DoctorAppointment.objects.filter(appointment_d=appoint).count()
    
    today_afternoon_patient=0
    for appoint in afternoon_appoint:
        today_afternoon_patient += DoctorAppointment.objects.filter(appointment_d=appoint).count()

    today_evening_patient=0
    for appoint in evening_appoint:
        today_evening_patient += DoctorAppointment.objects.filter(appointment_d=appoint).count()
    
    today_cancel_patient=0
    for appoint in cancel_appoint:
        today_cancel_patient +=DoctorAppointment.objects.filter(appointment_d=appoint).count()

    
    data_dic.update({
        'today_morning_patient':today_morning_patient,
        'today_afternoon_patient':today_afternoon_patient,
        'today_evening_patient':today_evening_patient,
        'today_cancel_patient':today_cancel_patient,
    })
    
    today_morning_prescribed=0
    for appoint in morning_appoint:
        today_morning_prescribed += DoctorAppointment.objects.filter(appointment_d=appoint,appointment_status=True).count()

    today_afternoon_prescribed=0
    for appoint in afternoon_appoint:
        today_afternoon_prescribed += DoctorAppointment.objects.filter(appointment_d=appoint,appointment_status=True).count()

    today_evening_prescribed=0
    for appoint in evening_appoint:
        today_evening_prescribed += DoctorAppointment.objects.filter(appointment_d=appoint,appointment_status=True).count()
    
    today_not_prescribed=0
    for appoint in today_appoint:
        today_not_prescribed += DoctorAppointment.objects.filter(appointment_d=appoint,appointment_status=False).count()

    data_dic.update({
        'today_morning_prescribed':today_morning_prescribed,
        'today_afternoon_prescribed':today_afternoon_prescribed,
        'today_evening_prescribed':today_evening_prescribed,
        'today_not_prescribed':today_not_prescribed,
    })

    morning_appointment=Appointment.objects.filter(time_slot='Morning(9.00am-1.00pm)',cancel_status=False)
    afternoon_appointment=Appointment.objects.filter(time_slot='Afternoon(4.00pm-6.30pm)',cancel_status=False)
    evening_appointment=Appointment.objects.filter(time_slot='Evening(7.30pm-8.30pm)',cancel_status=False)
    not_appointment=Appointment.objects.filter(cancel_status=False)
    cencel_appointment=Appointment.objects.filter(cancel_status=True)

    total_morning_prescribed=0
    total_afternoon_prescribed=0
    total_evening_prescribed=0
    total_not_prescribed=0

    for appointment in morning_appointment:
        total_morning_prescribed += DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=True).count()

    for appointment in afternoon_appointment:
        total_afternoon_prescribed += DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=True).count()

    for appointment in evening_appointment:
        total_evening_prescribed += DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=True).count()

    for appointment in not_appointment:
        total_not_prescribed += DoctorAppointment.objects.filter(appointment_d=appointment,appointment_status=False).count()
    
    data_dic.update({
        'total_morning_prescribed':total_morning_prescribed,
        'total_afternoon_prescribed':total_afternoon_prescribed,
        'total_evening_prescribed':total_evening_prescribed,
        'total_not_prescribed':total_not_prescribed,
    })

    total_cancel_patient=0
    for appointment in cencel_appointment:
        total_cancel_patient+=DoctorAppointment.objects.filter(appointment_d=appointment).count()
    

    total_appointment=DoctorAppointment.objects.all().count()

    prescribed_percentage=0.0
    not_prescribed_percentage=0.0
    cencel_percentage=0.0

    if total_appointment !=0:
        prescribed_percentage=(((total_morning_prescribed+total_afternoon_prescribed+today_evening_prescribed)/total_appointment)*100)
        not_prescribed_percentage=((today_not_prescribed/total_appointment)/100)
        cencel_percentage=((total_cancel_patient/total_appointment)*100)
    
    data_dic.update({
        'prescribed_percentage':prescribed_percentage,
        'not_prescribed_percentage':not_prescribed_percentage,
        'cencel_percentage':cencel_percentage
    })

    return render(request,'admin_app/patientStatics.html',context=data_dic)   