from unicodedata import name
from django.urls import path
from admin_app import views

app_name='admin_app'

urlpatterns = [
     path('admin_dash/',views.adminDashboard,name='admin_dash'),
     path('patient_list/',views.patientList,name='patient_list'),
     path('doctor_request/',views.doctorRequest,name='doctor_request'),
     path('add_doctor/<pk>/',views.addDoctor,name='add_doctor'),
     path('doctor_details/<pk>/',views.doctorDetail.as_view(),name='doctor_details'),
     path('doctor_list/',views.doctorList,name='doctor_list'),
     path('edit_doctor/<pk>',views.editDoctor.as_view(),name='edit_doctor'),
     path('prescribed_patient/',views.prescribedpatientList,name='prescribed_patient'),
     path('online_prescribed_patient/',views.onlinePrescribedpatientList,name='online_prescribed_patient'),
     path('prescribed_details/<int:pk>/',views.prescribedPatientDetails,name='prescribed_details'),
     path('online_prescribed_details/<int:pk>/',views.prescribedPatientDetails,name='online_prescribed_details'),
     path('patient_wating_report/',views.patientWaitReport,name='patient_wating_report'),
     path('online_patient_wating_report/',views.onlinePatientWaitReport,name='online_patient_wating_report'),
     path('submit_report/<int:pk>/',views.submitReport,name='submit_report'),
     path('submit_online_report/<int:pk>/',views.OnlineSubmitReport,name='submit_online_report'),
     path('todays_appointment/',views.todaysAppointmentList,name='todays_appointment'),
     path('all_appointment/',views.allAppointmentList,name='all_appointment'),
     path('add_catagory',views.addDoctorCatagory,name='add_catagory'),
     path('edit_catagory/<pk>/',views.updateCatagory.as_view(),name='edit_catagory'),
     path('delete_catagory/<pk>/',views.deleteCatagory.as_view(),name='delete_catagory'),
     path('user_request/',views.addUserRequest,name='user_request'),
     path('add_user/<int:pk>/',views.addUser,name='add_user'),
     path('doctor_report/',views.doctorReport,name='doctor_reprot'),
     path('doctor_report_details/<int:pk>/',views.doctorReportDetails,name='doctor_report_details'),
     path('doctor_from_to_report/<int:pk>/',views.searchFromTo,name='serarch_form_to'),
     path('doctor_statics/',views.doctorStatics,name='doctor_statics'),
     path('patient_statics/',views.patientStatics,name='patient_statics')
]
