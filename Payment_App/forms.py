from django import forms
from Payment_App.models import BillingAddress



class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        exclude =['user',]