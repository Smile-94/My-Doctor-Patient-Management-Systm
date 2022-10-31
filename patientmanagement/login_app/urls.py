
from django.urls import path
from login_app import views

app_name='login_app'

urlpatterns = [
    path('admin_arena/',views.adminClick,name='admin_arena'),
    path('doctor_arena/',views.doctorClick,name='doctor_arena'),
    path('patient_arena/',views.patientClick,name='patient_arena'),
    path('admin_signup/',views.adminSignUp,name='admin_singup'),
    path('admin_login/',views.loginAdmin,name='admin_login'),
    path('after_login/',views.afterlogin_view,name='after_login'),
    path('admin_info/',views.adminInfo,name='admin_info'),
    path('patient_login/',views.loginPatient,name='patient_login'),
    path('patient_signup/',views.patientSignup,name='patient_signup'),
    path('patient_info/',views.patientInfo,name='patient_info'),
    path('doctor_login/',views.loginDoctor,name='doctor_login'),
    path('doctor_signup/',views.doctorSignup,name='doctor_signup'),
    path('doctor_info/',views.doctorInfo,name='doctor_info'),
    path('logout_user/',views.logout_user,name='logout_user'), 
]
