from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.urls import reverse_lazy
from datetime import date

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate

from django.contrib.auth.models import Group
from django.conf import settings
from requests import request

#Forms and model
from login_app.models import Profile
from doctor_app.models import Appointment
from doctor_app.models import DoctorInfo
from doctor_app.models import OnlineAppointment
from doctor_app.forms import AppointmentForm, OnlineCancelForm
from doctor_app.forms import OnlineAppointmentForm
from doctor_app.forms import CancelForm
from appointment_app.models import DoctorAppointment, OnlineDoctorAppointment
from appointment_app.forms import DoctorAppointmentForm, OnlineDoctorAppointmentForm
from prescription_app.models import Prescription
from prescription_app.models import Reports
from prescription_app.models import Symptoms
from prescription_app.models import ReportFile
from prescription_app.models import OnlinePrescription
from prescription_app.models import OnlineReports
from prescription_app.models import OnlineSymptoms
from prescription_app.models import OnlineReportFile
from prescription_app.forms import PrescriptionForm
from prescription_app.forms import ReportsForm
from prescription_app.forms import SymptomsForm
from prescription_app.forms import OnlinePrescriptionForm
from prescription_app.forms import OnlineSymptomsForm
from prescription_app.forms import OnlineReportsForm
from prescription_app.forms import OnlineReportFileForm



# class based view
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView


#messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
@login_required
def doctorDashboard(request):
    
    doctor_info=DoctorInfo.objects.filter(user=request.user)
    doctor_info=doctor_info[0]

    pending_patient_count=DoctorAppointment.objects.filter(doctor_d=request.user,appointment_status=False).count()
    total_patient=DoctorAppointment.objects.filter(doctor_d=request.user,appointment_status=True).count()
    data_dic={
        'title':'Doctor Dashboard',
        'doctor_info':doctor_info,
        'total_pending':pending_patient_count,
        'total_patient':total_patient
        }

    #Todays All Patient
    if Appointment.objects.filter(appointment_date=date.today()).exists():
        appointment=Appointment.objects.filter(appointment_date=date.today())
        print(appointment)
       
        todays_appointment_count=0

        todays_patient=[]
        for appoint in appointment:
            todays_appointment_count +=DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d=appoint,added_to_appoint=True).count()
        
            todays_patient.extend(list(DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d=appoint,added_to_appoint=True,appointment_status=False).order_by('serial_number')))
        
        data_dic.update({'todays_ptient_count':todays_appointment_count,'todays_patient':todays_patient})

    #Todays Morning Patient
    if Appointment.objects.filter(appointment_date=date.today(),time_slot='Morning(9.00am-1.00pm)').exists():
        morning_slot=Appointment.objects.filter(appointment_date=date.today(),time_slot='Morning(9.00am-1.00pm)')
        morning_patient=[]
        for morning in morning_slot:
            morning_patient.extend(list(DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d=morning,added_to_appoint=True,appointment_status=False).order_by('serial_number'))) 
            print("This is morning slot")
        print("Morning slot object",morning_patient)
        data_dic.update({'morning_patient':morning_patient})
        
    #Todays Afternoon Patinet
    if Appointment.objects.filter(appointment_date=date.today(),time_slot='Afternoon(4.00pm-6.30pm)').exists():
        
        afternoon_slot=Appointment.objects.filter(appointment_date=date.today(),time_slot='Afternoon(4.00pm-6.30pm)')
        print("After noon slot: ",afternoon_slot)
        afternoon_patient=[]
        for afternoon in afternoon_slot:
            afternoon_patient.extend(list(DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d=afternoon,added_to_appoint=True,appointment_status=False).order_by('serial_number'))) 
        data_dic.update({'afternoon_patient':afternoon_patient})

    #Todays Evening Patient
    if Appointment.objects.filter(appointment_date=date.today(),time_slot='Evening(7.30pm-8.30pm)').exists():
        evening_slot=Appointment.objects.filter(appointment_date=date.today(),time_slot='Evening(7.30pm-8.30pm)')

        evening_patient=[]
        for evening in evening_slot:
            evening_patient.extend(list(DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d= evening,added_to_appoint=True,appointment_status=False).order_by('serial_number'))) 
        data_dic.update({'evening_patient':evening_patient})

    
    return render(request,'doctor_app/doctorDash.html',context=data_dic)

@login_required
def doctorProfile(request):
    doctor_info=DoctorInfo.objects.filter(user=request.user)
    doctor_info=doctor_info[0]
    data_dic={'title':'Doctor Profile','doctor_info':doctor_info}
    return render(request,'doctor_app/profileDoctor.html',context=data_dic)

@method_decorator(login_required,name='dispatch')
class editDoctorBasicInfo(SuccessMessageMixin, UpdateView):
    fields=('fullName','gender','user_phone','user_photo')
    model=Profile
    success_url=reverse_lazy('doctor_app:doctor_profile')
    template_name='doctor_app/editdoctorBasicInfo.html'
    success_message="Your Basic Information updated successfully"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Edit Basic Info'

        return context

@method_decorator(login_required,name='dispatch')
class editDoctorPersonalInfo(SuccessMessageMixin, UpdateView):
    fields=('title','doctor_type','specialist','road','sector','city','postcode','doctor_sort_description')
    model=DoctorInfo
    success_url=reverse_lazy('doctor_app:doctor_profile')
    template_name='doctor_app/editdoctorParsonalInfo.html'
    success_message="Your Personal Information updated successfully"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Edit Personal Info'

        return context


@login_required
def pendingGiveTime(request):
    data_dic={}
    #Morning patinet wait for Time
    if Appointment.objects.filter(time_slot='Morning(9.00am-1.00pm)').exists():
        morning_slot=Appointment.objects.filter(time_slot='Morning(9.00am-1.00pm)')

        give_time_morning=[]
        for morning in morning_slot:
            give_time_morning.extend(list(DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d=morning,added_to_appoint=True,appointment_status=False,appointment_time=None).order_by('serial_number')))
        data_dic.update({'morning_time_give':give_time_morning})   
       
    #Afternoon patinet wait for Time
    if Appointment.objects.filter(time_slot='Afternoon(4.00pm-6.30pm)').exists():
        afternoon_slot=Appointment.objects.filter(time_slot='Afternoon(4.00pm-6.30pm)')

        give_time_afternoon=[]
        for afternoon in afternoon_slot:
            give_time_afternoon.extend(list(DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d= afternoon,added_to_appoint=True,appointment_status=False,appointment_time=None).order_by('serial_number')))
        
        data_dic.update({'afternoon_time_give':give_time_afternoon})
       
    #Evening patinet wait for Time
    if Appointment.objects.filter(time_slot='Evening(7.30pm-8.30pm)').exists():
        evening_slot=Appointment.objects.filter(time_slot='Evening(7.30pm-8.30pm)')

        give_time_evening=[]
        for evening in evening_slot:
            give_time_evening.extend(list(DoctorAppointment.objects.filter(doctor_d=request.user,appointment_d=evening,added_to_appoint=True,appointment_status=False,appointment_time=None).order_by('serial_number')))

        
        data_dic.update({'evening_time_give':give_time_evening})  
       
        
   
    pending_patient=DoctorAppointment.objects.filter(doctor_d=request.user,added_to_appoint=True,appointment_status=False,appointment_time=None).order_by('serial_number')
    time_form=DoctorAppointmentForm()
    data_dic.update({'title':'Give Time','pending_patient':pending_patient,'form':time_form} )
    return render(request,'doctor_app/pendingPatient.html',context=data_dic,)

@login_required
def onlinePendingGiveTime(request):
    data_dic={}
    
    pending_patient=OnlineDoctorAppointment.objects.filter(online_doctor_d=request.user,online_appointment_status=False,online_appointment_time=None).order_by('online_serial_number')
    time_form=OnlineDoctorAppointmentForm()
    data_dic.update({'title':'Give Time','pending_patient':pending_patient,'form':time_form} )
    return render(request,'doctor_app/onlinePendingPatient.html',context=data_dic,)

@login_required
def giveTime(request,pk):
    time_object=DoctorAppointment.objects.get(id=pk)
    form=DoctorAppointmentForm(instance=time_object)
    if request.method =='POST':
        form=DoctorAppointmentForm(request.POST, instance=time_object)

        if form.is_valid():
            if form is not None and form!=' ':
                form.save()
                print("Valid Form",form)
                messages.success(request,'Update time successfully')
                return HttpResponseRedirect(reverse('doctor_app:pending_patient_time'))
    
    messages.warning(request,'Something Happend Try Againg')
    return HttpResponseRedirect(reverse('doctor_app:pending_patient_time'))

@login_required
def onlineGiveTime(request,pk):
    time_object=OnlineDoctorAppointment.objects.get(id=pk)
    form=OnlineDoctorAppointmentForm(instance=time_object)
    if request.method =='POST':
        form=OnlineDoctorAppointmentForm(request.POST, instance=time_object)

        if form.is_valid():
            if form is not None and form!=' ':
                form.save()
                messages.success(request,'Update time successfully')
                return HttpResponseRedirect(reverse('doctor_app:online_pending_patient_time'))
    
    messages.warning(request,'Something Happend Try Againg')
    return HttpResponseRedirect(reverse('doctor_app:online_pending_patient_time'))

    

@login_required
def createAppointmnet(request):
    appoint_form=AppointmentForm()
    data_dic={'title':'Create Appointment','appoint_form':appoint_form}
    

    if request.method=='POST':
        appoint_form=AppointmentForm(request.POST)
        appoint_form.instance.user=request.user
        appoint_form.instance.appoint_user_id=request.user.id
        appoint_form.save()
       
        if appoint_form.is_valid():
            appoint_form.save()
            messages.success(request,'Appointment Date added successfully')
            return HttpResponseRedirect(reverse('doctor_app:appointment'))
        messages.warning("Try againg with field all the field")
    return render(request,'doctor_app/createAppointment.html',context=data_dic)

 
class editAppointment(SuccessMessageMixin,UpdateView):
    fields = ("appointment_date","time_slot","room_number","hospital_name","number_of_patient","active_status")
    model=Appointment
    success_url=reverse_lazy('doctor_app:appointment_list')
    template_name='doctor_app/edit_appointment.html'
    success_message="Appointment update successfully"
    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Edit Appointment Info'

        return context

def cancelAppointment(request,pk):
    data_dic={'title':'Cancel Appointment'}
    appointment=Appointment.objects.get(id=pk)
    form=CancelForm(instance=appointment)
    data_dic.update({'form':form})

    if request.method=='POST':
        form=CancelForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            appointment.cancel_status=True
            appointment.save()
            return HttpResponseRedirect(reverse('doctor_app:appointment_list'))

    return render(request,'doctor_app/cancelAppointForm.html',context=data_dic)

@login_required
def appointmentList(request):
    data_dic={'title':'Appointment List'}

    appointment_list=Appointment.objects.filter(appoint_user=request.user,cancel_status=False).order_by('-id')
    data_dic.update({'appointment_list':appointment_list})

    return render(request, 'doctor_app/appointList.html',context=data_dic)


@login_required
def createOnlineAppointment(request):
    online_appoint_form=OnlineAppointmentForm()
    data_dic={'title':'Create Appointment','online_appoint_form':online_appoint_form}
    

    if request.method=='POST':
        online_appoint_form=OnlineAppointmentForm(request.POST)
        online_appoint_form.instance.appointment_user=request.user
        online_appoint_form.save()
       
        if online_appoint_form.is_valid():
            online_appoint_form.save()
            messages.success(request,'Appointment Date added successfully')
            return HttpResponseRedirect(reverse('doctor_app:online_appointment'))
        messages.warning("Try againg with field all the field")
    return render(request,'doctor_app/onlineAppointmentForm.html',context=data_dic)    

class editOnlineAppointment(SuccessMessageMixin,UpdateView):
    fields = ("online_appointment_date","online_time_slot","online_number_of_patient","online_active_status","zoom_link",)
    model=OnlineAppointment
    success_url=reverse_lazy('doctor_app:online_appoint_list')
    template_name='doctor_app/edit_online_appointment.html'
    success_message="Appointment update successfully"

def cancelOnlineAppointment(request,pk):
    data_dic={'title':'Cancel Appointment'}
    online_appointment=OnlineAppointment.objects.get(id=pk)
    online_form=OnlineCancelForm(instance=online_appointment)
    data_dic.update({'online_form':online_form})
    print(data_dic)

    if request.method=='POST':
        online_form=OnlineCancelForm(request.POST, instance=online_appointment)
        if online_form.is_valid():
            online_form.save()
            online_appointment.online_cancel_status=True
            online_appointment.save()
            return HttpResponseRedirect(reverse('doctor_app:online_appoint_list'))

    return render(request,'doctor_app/onlineCancelAppoinFor.html',context=data_dic)

@login_required
def OnlineAppointmentList(request):
    data_dic={'title':'Appointment List'}

    online_appointment_list=OnlineAppointment.objects.filter(appointment_user=request.user,online_cancel_status=False).order_by('-id')
    data_dic.update({'online_appointment_list':online_appointment_list})

    return render(request, 'doctor_app/onlineAppointmentList.html',context=data_dic)

def symptoms_details(request,pk):
    data_dic={'title':'Symptoms Details'}
    appointment=DoctorAppointment.objects.get(id=pk)
    symtomps_form=SymptomsForm(instance=appointment)
    data_dic.update({'symtomps_form':symtomps_form})

    if request.method=='POST':
        symtomps_form=SymptomsForm(request.POST)
        symtomps_form.instance.symptoms_for=appointment
        symtomps_form.save()
        if symtomps_form.is_valid():
            symtomps_form.save()
            messages.success(request,'Patientn Basic info updated successfully')
            url='/doctor/prescription/{pk}/'.format(pk=pk)
            return redirect(url)


    return render(request,'doctor_app/symtomsForm.html',context=data_dic)

@login_required
def prescription(request,pk):
    
    data_dic={}
    appointment=DoctorAppointment.objects.get(id=pk)

    prescription_form=PrescriptionForm(instance=appointment)

    data_dic.update({'title':'prescription','form':prescription_form,'pk':pk})

    if request.method=='POST':
        prescription_form=PrescriptionForm(request.POST)
        prescription_form.instance.prescription_for=appointment
        prescription_form.save()
        
        if prescription_form.is_valid():
            prescription_form.save(commit=True)
            
            messages.success(request,"Medicine Added Successfully")

    appointment_obj=DoctorAppointment.objects.get(id=pk)
    medicine_list=Prescription.objects.filter(prescription_for=appointment_obj)
    data_dic.update({'medicine_list':medicine_list})
    
    return render(request,'doctor_app/prescription.html',context=data_dic)

@login_required
def editMedicine(request,pk,pk2):
    data_dic={'title':'Edit Medicine'}

    medicine=Prescription.objects.get(id=pk)
    form=PrescriptionForm(instance=medicine)
    data_dic.update({'form':form})

    if request.method=='POST':
        form=PrescriptionForm(request.POST,instance=medicine)

        if form.is_valid():
            form.save()
            url=url='/doctor/prescription/{pk}/'.format(pk=pk2)
            return redirect(url)

    return render(request,'doctor_app/editMedicine.html',context=data_dic)

def deleteMedicine(request,pk,pk2):
    data_dic={'title':'Delete Mediciene'}

    object=get_object_or_404(Prescription, id=pk)
    data_dic.update({'medicine':object})

    if request.method=='POST':
        object.delete()

        url=url='/doctor/prescription/{pk}/'.format(pk=pk2)
        return redirect(url)

    return render(request,'doctor_app/deleteMedicine.html',context=data_dic)


@login_required
def reports(request,pk):
    data_dic={'title':'Prescribe Reporst'}
    appointment=DoctorAppointment.objects.get(id=pk)
    data_dic.update({'appointment':appointment})
    
    

    reports_form=ReportsForm(instance=appointment)
    data_dic.update({'reports_form':reports_form})

    appointment.appointment_status=True
    appointment.save()

    if request.method=='POST':
        reports_form=ReportsForm(request.POST)
        reports_form.instance.report_for_id=appointment.id 
        reports_form.save()

        
        if reports_form.is_valid():
            reports_form.save()

            reports_form.instance.report_for=appointment
            reports_form.save()
            messages.success(request,'Reports Added Successfully')

    appointment_obj=DoctorAppointment.objects.get(id=pk)
    report_list=Reports.objects.filter(report_for=appointment_obj)
    data_dic.update({'report_list':report_list})


    return render(request,'doctor_app/reportForm.html',context=data_dic)

#Edit off line report function
@login_required
def editReport(request,pk,pk2):
    data_dic={'title':'Edit Report'}

    report=Reports.objects.get(id=pk)
    report_form=ReportsForm(instance=report)
    data_dic.update({'report_form':report_form})

    if request.method=='POST':
        report_form=ReportsForm(request.POST,instance=report)

        if report_form.is_valid():
            report_form.save()
            messages.success(request,'Report Update Successfully')
            url=url='/doctor/report_form/{pk}/'.format(pk=pk2)
            return redirect(url)

    return render(request,'doctor_app/editMedicine.html',context=data_dic)

#Delete off line report function
@login_required
def deleteReport(request,pk,pk2):
    data_dic={'title':'Delete Mediciene'}

    report_object=get_object_or_404(Reports, id=pk)
    data_dic.update({'report_object':report_object})

    if request.method=='POST':
        report_object.delete()

        messages.success(request,'Report Delete Successfully')
        url=url='/doctor/report_form/{pk}/'.format(pk=pk2)
        return redirect(url)

    return render(request,'doctor_app/deleteMedicine.html',context=data_dic)


@login_required
def pendingPaitentList(request):
    data_dic={'title':'Pending Paient List'}

    if DoctorAppointment.objects.filter(doctor_d=request.user,appointment_status=False).exists():
        pending_patient=DoctorAppointment.objects.filter(doctor_d=request.user,appointment_status=False).order_by('serial_number')
        data_dic.update({'pending_patient':pending_patient})


    return render(request,'doctor_app/pendingPatientList.html',context=data_dic)

@login_required
def onlinePendingPaitentList(request):
    data_dic={'title':'Pending Paient List'}

    if OnlineDoctorAppointment.objects.filter(online_doctor_d=request.user,online_appointment_status=False).exists():
        pending_patient=OnlineDoctorAppointment.objects.filter(online_doctor_d=request.user,online_appointment_status=False)
        data_dic.update({'pending_patient':pending_patient})


    return render(request,'doctor_app/onlinePendingPatList.html',context=data_dic)

@login_required
def pendingPatientDetail(request,pk):
    data_dic={'title':'Patient Detail'}

    patient_details=DoctorAppointment.objects.get(doctor_d=request.user,appointment_status=False,id=pk)
    data_dic.update({'patient_details':patient_details})

   

    return render(request,'doctor_app/pendingPatientDetails.html',context=data_dic)

@login_required
def OnlinePendingPatientDetail(request,pk):
    data_dic={'title':'Patient Detail'}

    patient_details=OnlineDoctorAppointment.objects.get(online_doctor_d=request.user,online_appointment_status=False,id=pk)
    data_dic.update({'patient_details':patient_details})


    return render(request,'doctor_app/onlinePendingPatDetails.html',context=data_dic)

@login_required
def prescribedPatientList(request):
    data_dic={'title':'Prescribed Patient'}

    if DoctorAppointment.objects.filter(doctor_d=request.user,appointment_status=True).exists():
        prescribed_patient=DoctorAppointment.objects.filter(doctor_d=request.user,appointment_status=True).order_by('-id')
        data_dic.update({'prescribed_patient':prescribed_patient})
    
    return render(request,'doctor_app/prescribedPatientList.html',context=data_dic)


@login_required
def prescribePatientDetail(request,pk):
    data_dic={'title':'Patient Details'}

    prescribe_patient_details=DoctorAppointment.objects.get(doctor_d=request.user,appointment_status=True,id=pk)
    data_dic.update({'patient_details':prescribe_patient_details})

    patient_symptoms=Symptoms.objects.get(symptoms_for=prescribe_patient_details)
    data_dic.update({'patient_symptoms':patient_symptoms})

    patient_prescription=Prescription.objects.filter(prescription_for=prescribe_patient_details)
    data_dic.update({'patient_prescription':patient_prescription})

    reports_details=Reports.objects.filter(report_for=prescribe_patient_details)
    data_dic.update({'reports_details':reports_details})

    report_file=ReportFile.objects.filter(file_for=prescribe_patient_details)
    data_dic.update({'report_file':report_file})

    return render(request,'doctor_app/prescribePatientDetails.html',context=data_dic)

@login_required
def prescribeOnlinePatient(request):
    data_dic={'title':'Online Patient'}

    if OnlineAppointment.objects.filter(online_appointment_date=date.today()).exists():
        appointment=OnlineAppointment.objects.filter(online_appointment_date=date.today())
       
    
        todays_patient=[]
        for appoint in appointment:
            todays_patient.extend(list(OnlineDoctorAppointment.objects.filter(online_doctor_d=request.user,online_appointment_d=appoint,online_appointment_status=False).order_by('online_serial_number')))
        
        data_dic.update({'todays_patient':todays_patient})
    return render(request,'doctor_app/prescribeOnlinePatient.html',context=data_dic)


def onlineSymptomsDetails(request,pk):
    data_dic={'title':'Symptoms Details'}
    appointment=OnlineDoctorAppointment.objects.get(id=pk)
    symtomps_form=OnlineSymptomsForm(instance=appointment)
    data_dic.update({'symtomps_form':symtomps_form})

    if request.method=='POST':
        symtomps_form=OnlineSymptomsForm(request.POST)
        symtomps_form.instance.online_symptoms_for=appointment
        symtomps_form.save()
        if symtomps_form.is_valid():
            symtomps_form.save()
            messages.success(request,'Patientn Basic info updated successfully')
            url='/doctor/online_prescription/{pk}/'.format(pk=pk)
            return redirect(url)

    return render(request,'doctor_app/onlineSymtomsForm.html',context=data_dic)

def onlinePrescription(request,pk):
    data_dic={}
    appointment=OnlineDoctorAppointment.objects.get(id=pk)

    prescription_form=OnlinePrescriptionForm()

    data_dic.update({'title':'Online prescription','form':prescription_form,'pk':pk})

    if request.method=='POST':
        prescription_form=OnlinePrescriptionForm(request.POST)
        prescription_form.instance.Online_prescription_for=appointment
        prescription_form.save()
        
        if prescription_form.is_valid():
            prescription_form.save(commit=True)
            
            messages.success(request,"Medicine Added Successfully")

    appointment_obj=OnlineDoctorAppointment.objects.get(id=pk)
    medicine_list=OnlinePrescription.objects.filter(Online_prescription_for=appointment_obj)
    data_dic.update({'medicine_list':medicine_list})
    
    return render(request,'doctor_app/onlinePrescription.html',context=data_dic)

@login_required
def editOnlineMedicine(request,pk,pk2):
    data_dic={'title':'Edit Medicine'}

    medicine=OnlinePrescription.objects.get(id=pk)
    form=OnlinePrescriptionForm(instance=medicine)
    data_dic.update({'form':form})

    if request.method=='POST':
        form=OnlinePrescriptionForm(request.POST,instance=medicine)

        if form.is_valid():
            form.save()
            url=url='/doctor/online_prescription/{pk}/'.format(pk=pk2)
            return redirect(url)

    return render(request,'doctor_app/editOnlineMedicine.html',context=data_dic)

def deleteOnlineMedicine(request,pk,pk2):
    data_dic={'title':'Delete Mediciene'}

    object=get_object_or_404(OnlinePrescription, id=pk)
    data_dic.update({'medicine':object})

    if request.method=='POST':
        object.delete()

        url=url='/doctor/online_prescription/{pk}/'.format(pk=pk2)
        return redirect(url)

    return render(request,'doctor_app/deleteOnlineMedicine.html',context=data_dic)

@login_required
def onlineReports(request,pk):
    data_dic={'title':'Prescribe Reporst'}

    appointment=OnlineDoctorAppointment.objects.get(id=pk)
    data_dic.update({'appointment':appointment})
    
    reports_form=OnlineReportsForm(instance=appointment)
    data_dic.update({'reports_form':reports_form})

    if request.method=='POST':
        reports_form=OnlineReportsForm(request.POST)
        reports_form.instance.online_report_for=appointment 
        reports_form.save()
        
        if reports_form.is_valid():
            reports_form.save(commit=True)

            appointment.online_appointment_status=True
            appointment.save()
            messages.success(request,'Reports Added Successfully')

    appointment_obj=OnlineDoctorAppointment.objects.get(id=pk)
    report_list=OnlineReports.objects.filter(online_report_for=appointment_obj)
    data_dic.update({'report_list':report_list})


    return render(request,'doctor_app/onlineReportForm.html',context=data_dic)

@login_required
def editOnlineReport(request,pk,pk2):
    data_dic={'title':'Edit Report'}

    report=OnlineReports.objects.get(id=pk)
    report_form=OnlineReportsForm(instance=report)
    data_dic.update({'report_form':report_form})

    if request.method=='POST':
        report_form=OnlineReportsForm(request.POST,instance=report)

        if report_form.is_valid():
            report_form.save()
            messages.success(request,'Report Update Successfully')
            url=url='/doctor/online_reoprt_form/{pk}/'.format(pk=pk2)
            return redirect(url)

    return render(request,'doctor_app/editOnlineMedicine.html',context=data_dic)

@login_required
def deleteOnlineReport(request,pk,pk2):
    data_dic={'title':'Delete Mediciene'}

    report_object=get_object_or_404(OnlineReports, id=pk)
    data_dic.update({'report_object':report_object})

    if request.method=='POST':
        report_object.delete()

        messages.success(request,'Report Delete Successfully')
        url=url='/doctor/online_reoprt_form/{pk}/'.format(pk=pk2)
        return redirect(url)

    return render(request,'doctor_app/deleteOnlineMedicine.html',context=data_dic)

#Online prescribed patient list function
@login_required
def onlinePrescribedPatientList(request):
    data_dic={'title':'Prescribed Patient'}

    if OnlineDoctorAppointment.objects.filter(online_doctor_d=request.user,online_appointment_status=True).exists():
        prescribed_patient=OnlineDoctorAppointment.objects.filter(online_doctor_d=request.user,online_appointment_status=True).order_by('-id')
        data_dic.update({'prescribed_patient':prescribed_patient})
    
    return render(request,'doctor_app/onlinePrescribedPatientList.html',context=data_dic)

#Online prescribed patient details
@login_required
def onlinePrescribePatientDetail(request,pk):
    data_dic={'title':'Patient Details'}

    prescribe_patient_details=OnlineDoctorAppointment.objects.get(online_doctor_d=request.user,online_appointment_status=True,id=pk)
    data_dic.update({'patient_details':prescribe_patient_details})

    if OnlineSymptoms.objects.get(online_symptoms_for=prescribe_patient_details).exists():
        patient_symptoms=OnlineSymptoms.objects.get(online_symptoms_for=prescribe_patient_details)
        data_dic.update({'patient_symptoms':patient_symptoms})

    if OnlinePrescription.objects.filter(Online_prescription_for=prescribe_patient_details).exists():
        patient_prescription=OnlinePrescription.objects.filter(Online_prescription_for=prescribe_patient_details)
        data_dic.update({'patient_prescription':patient_prescription})

    reports_details=OnlineReports.objects.filter(online_report_for=prescribe_patient_details)
    data_dic.update({'reports_details':reports_details})

    report_file=OnlineReportFile.objects.filter(online_file_for=prescribe_patient_details)
    data_dic.update({'report_file':report_file})

    return render(request,'doctor_app/onlinePrescribedPatDetails.html',context=data_dic)