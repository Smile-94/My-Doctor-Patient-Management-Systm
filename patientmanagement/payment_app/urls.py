from django.urls import path
from payment_app import views

app_name='payment_app'

urlpatterns = [

    path('payment/<int:pk>/',views.payment,name='payment'),
    path('status/<int:pk>/',views.complete,name='complete'),
    path('payment_status/<int:pk>/<str:tran_id>/<str:val_id>/',views.payemtSatus,name='payment_status')
    
]