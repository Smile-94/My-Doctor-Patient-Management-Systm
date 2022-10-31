from django import forms
from django.forms import ModelForm

from payment_app.models import PaymentStatus

class PaymentStatusForm(forms.ModelForm):
    
    class Meta:
        model=PaymentStatus
        fields=('payment_status',)