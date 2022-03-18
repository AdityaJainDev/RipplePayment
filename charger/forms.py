from django import forms

class MakePayment(forms.Form):
    address = forms.CharField(label="Address to Send", required = False)
    amount = forms.CharField(label="Amount", required = False)
    
