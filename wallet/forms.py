from django import forms

class Details(forms.Form):
    url = forms.CharField(label="Please enter the link provided by the charger", required = False)

class PaymentDetail(forms.Form):
    address = forms.CharField(label="Address to Send", required = False)
    amount = forms.CharField(label="Amount", required = False)
    
