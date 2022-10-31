from django.urls import path

from home_app import views

app_name='home_app'

urlpatterns = [
    path('',views.index,name="home"),
    path('singup_or_login',views.signUpRequest,name="singup_or_login"),
    
]