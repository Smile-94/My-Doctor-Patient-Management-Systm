
from unicodedata import name
from django.urls import path
from doctor_app import views

app_name='doctor_app'

urlpatterns = [
    path('doctor_dash/',views.doctorDashboard,name='doctor_dash'),
    path('doctor_profile/',views.doctorProfile,name='doctor_profile') ,
    path('edit_doctor_basic/<pk>/',views.editDoctorBasicInfo.as_view(),name='edit_doctor_basic'),
    path('edit_doctor/<pk>/',views.editDoctorPersonalInfo.as_view(),name='edit_doctor'),
    path('appointment/',views.createAppointmnet,name='appointment'),
    path('appointment_list/',views.appointmentList,name='appointment_list'),
    path('edit_appointment/<pk>/',views.editAppointment.as_view(),name='edit_appointment'),
    path('cancel_appointment/<int:pk>/',views.cancelAppointment,name='cancel_appointment'),
    path('online_appointment/',views.createOnlineAppointment,name='online_appointment'),
    path('online_cancel_appoint/<int:pk>/',views.cancelOnlineAppointment,name='online_cancel_appoint'),
    path('online_appoint_list/',views.OnlineAppointmentList,name='online_appoint_list'),
    path('edit_online_appoint/<pk>/',views.editOnlineAppointment.as_view(),name='edit_online_appoint'),
    path('pending_patient_time/',views.pendingGiveTime,name='pending_patient_time'),
    path('online_pending_patient_time/',views.onlinePendingGiveTime,name='online_pending_patient_time'),
    path('give_tme/<int:pk>/',views.giveTime,name='give_time'),
    path('online_give_tme/<int:pk>/',views.onlineGiveTime,name='online_give_time'),
    path('symptoms_form/<int:pk>/',views.symptoms_details,name='symptoms_form'),
    path('prescription/<int:pk>/',views.prescription,name='prescription'),
    path('edit_medicine/<int:pk>/<int:pk2>/',views.editMedicine,name='editi_medicine'),
    path('delete_medicine/<int:pk>/<int:pk2>',views.deleteMedicine,name='delete_medicine'),
    path('report_form/<int:pk>/',views.reports,name='report_form'),
    path('edit_report/<int:pk>/<int:pk2>/',views.editReport,name='edit_report'),
    path('delete_report/<int:pk>/<int:pk2>/',views.deleteReport,name='delete_report'),
    path('pending_pat_list/',views.pendingPaitentList,name='pending_pat_list'),
    path('online_pending_pat_list/',views.onlinePendingPaitentList,name='online_pending_pat_list'),
    path('pending_pat_details/<int:pk>/',views.pendingPatientDetail,name='pending_pat_details'),
    path('online_pending_pat_details/<int:pk>/',views.OnlinePendingPatientDetail,name='online_pending_pat_details'),
    path('prescribed_pat_list/',views.prescribedPatientList,name='prescribed_pat_list'),
    path('prescribed_pat_details/<int:pk>/',views.prescribePatientDetail,name='prescribed_pat_details'),
    path('prescribe_online_patient/',views.prescribeOnlinePatient,name='prescribe_online_patient'),
    path('online_symptoms_form/<int:pk>/',views.onlineSymptomsDetails,name='online_symptoms_form'),
    path('online_prescription/<int:pk>/',views.onlinePrescription,name='online_prescription'),
    path('edit_online_medicine/<int:pk>/<int:pk2>/',views.editOnlineMedicine,name='editi_online_medicine'),
    path('delete_online_medicine/<int:pk>/<int:pk2>/',views.deleteOnlineMedicine,name='delete_online_medicine'),
    path('online_reoprt_form/<int:pk>/',views.onlineReports,name='online_report_form'),
    path('edit_online_report/<int:pk>/<int:pk2>/',views.editOnlineReport,name='edit_online_report'),
    path('delete_online_report/<int:pk>/<int:pk2>/',views.deleteOnlineReport,name='delete_online_report'),
    path('online_prescribed_pat_list/',views.onlinePrescribedPatientList,name='online_prescribed_pat_list'),
    path('online_prescribed_pat_details/<int:pk>/',views.onlinePrescribePatientDetail,name='online_prescribed_pat_details'),
    
]