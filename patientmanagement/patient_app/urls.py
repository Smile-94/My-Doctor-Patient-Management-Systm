
from django.urls import path
from patient_app import views

app_name='patient_app'

urlpatterns = [
    path('patient_dash/',views.patientDashboard,name='patient_dash'),
    path('patient_profile/',views.patientProfile,name='patient_profile'),
    path('edit_basic/<pk>/',views.editBasicInfo.as_view(),name='edit_basic'),
    path('edit_parsonal/<pk>/',views.editPersonalInfo.as_view(),name='edit_parsonal'),
    path('find_doctor/',views.findDoctor,name='find_doctor'),
    path('find_catagory_doctor/<int:pk>/',views.findDoctorCatagory,name='find_catagory_doctor'),
    path('make_appointmnet/<int:pk>/',views.makeAppointment,name='make_appointment'),
    path('confirm_appointment/<int:doctor>/<int:appointment>/',views.confirmAppointment,name='confirm_appointment'),
    path('confirm_online_appointment/<int:doctor>/<int:appointment>/',views.confirmOnlineAppointment,name='confirm_online_appointment'),
    path('appointment_history/',views.appointmentHistory,name='appointment_history'),
    path('appointment_details/<pk>/',views.appointmentDetails,name='appointment_details'),
    path('online_appointment_details/<pk>/',views.onlineAppointmentDetails,name='online_appointment_details'),
    path('confirm_payment/<int:pk>/',views.conformPayment,name='confirm_payment'),
    path('recent_prescription/',views.recentPrescription,name='recent_prescription'),
    path('prescription_list/',views.prescriptionList,name='Prescription_list'),
    path('online_prescription_list/',views.onlinePrescriptionList,name='online_Prescription_list'),
    path('prescription_details/<int:pk>/',views.prescriptionDetails,name='prescription_details'),
    path('online_prescription_details/<int:pk>/',views.onlinePrescriptionDetails,name='online_prescription_details'),
    
    


]