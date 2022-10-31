from logging.config import valid_ident
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse



from django.contrib import messages


from django.contrib.auth.decorators import login_required

from login_app.models import Profile
from patient_app.models import PatientInfo
from payment_app.models import PaymentStatus
from payment_app.forms import PaymentStatusForm
from appointment_app.models import OnlineDoctorAppointment
from payment_app.forms import PaymentStatusForm




#for payment
import socket
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def payment(request,pk):
    stor_id='trian62cc10ef4bb1f'
    API_key='trian62cc10ef4bb1f@ssl'

    url='/payments/status/{pk}/'.format(pk=pk)
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=stor_id, sslc_store_pass=API_key)


   
    status_url=request.build_absolute_uri(url)
    # status_url=request.build_absolute_uri(reverse('payment_app:complete'))
    cancel_url=request.build_absolute_uri(reverse('patient_app:appointment_history'))
    # fali_url=request.build_absolute_uri(reverse('payment_app:payment'))
    mypayment.set_urls(success_url=status_url, fail_url=cancel_url, cancel_url=cancel_url)


    mypayment.set_product_integration(total_amount=Decimal(500), currency='BDT', product_category='Mixed', product_name='Prescription', num_of_item=1, shipping_method='None', product_profile='None')

    current_user=request.user

    mypayment.set_customer_info(name=current_user.profile.fullName, email=current_user.email, address1='Dhaka', address2='Dhaka', city='Dhaka', postcode='1230', country='Bangladesh', phone=current_user.profile.user_phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.fullName, address='Dhaka', city='Dhaka', postcode='Dhaka', country='Bangladesh')

    response_data = mypayment.init_payment()

    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complete(request,pk):
    form=PaymentStatusForm()
    if request.method=='POST' or request.method=='post':
        payment_data=request.POST
        status=payment_data['status']
        
        
        if status=='VALID':
            tran_id=payment_data['tran_id']
            val_id=payment_data['val_id']

            messages.success(request,'Your payment completed success fully')
        elif status=='FAILD':
            messages.warning(request, "Your payment not complete, please try againg")
    return render(request,'payment_app/paymentComplete.html',context={'tran_id':tran_id,'val_id':val_id,'form':form,'pk':pk})

@login_required
def payemtSatus(request,pk,tran_id,val_id):
    appointment=OnlineDoctorAppointment.objects.get(id=pk)
    payment=PaymentStatus.objects.filter(payment_user=request.user,payment_appointment=appointment)
    payment=payment[0]
    payment.tran_id=tran_id
    payment.valid_id=val_id
    payment.save()
    return HttpResponseRedirect(reverse('patient_app:appointment_history'))

    
   

    

    
    

    


