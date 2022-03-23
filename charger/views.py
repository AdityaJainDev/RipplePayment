from multiprocessing import context
from pprint import pprint
from django.shortcuts import render
from .forms import MakePayment
import requests
import json
from django.shortcuts import redirect
import xrpl
import time
import pyshorteners
# Create your views here.

# Generate Wallet
##################################
# from xrpl.wallet import generate_faucet_wallet, Wallet
# test_wallet = generate_faucet_wallet(client, debug=True)
# print(test_wallet)
# print(test_wallet.seed, test_wallet.sequence)
##################################

address_charger = "rEVpYkfg2VSh4Tco6GN5uciWvdt6cusSkh"

testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

def create_payment(request):
    if request.method == 'GET':
        form = MakePayment()

    elif request.method == 'POST':
        form = MakePayment(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            amount = form.cleaned_data['amount']

            if address == "":
                address = address_charger

            payment_object = {
                "address" : address,
                "amount" : amount
            }

            url_new = "https://api.npoint.io/67a6d648e336c1082719"

            requests.post(url_new, data=json.dumps(payment_object))

            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(url_new)

            request.session['url_new'] = short_url.rsplit('/', 1)[1]

            balance_old = xrpl.account.get_balance(address_charger, client)

            request.session['balance_old'] = balance_old

            return redirect("charger:show_details")


    context = {"form": form, "address_charger": address_charger}
    return render(request, "charger/create_payment.html", context)


def show_details(request):
    return render(request, "charger/show_details.html")
    

def transactions(request):

    info2 = xrpl.account.get_account_payment_transactions(address_charger, client)
    info1 = xrpl.account.get_balance(address_charger, client)

    context = {"transactions":info2, "balance": info1}
    
    return render(request, "charger/transactions.html", context)

def new_details(request):
    
    info2 = xrpl.account.get_account_payment_transactions(address_charger, client)
    
    balance_old = request.session['balance_old']
    balance_new = xrpl.account.get_balance(address_charger, client)
    
    timeout = time.time() + 1   # 5 minutes from now
    while balance_old == balance_new:
        balance_new = xrpl.account.get_balance(address_charger, client)
        if balance_new != balance_old or time.time() > timeout:
            
            return redirect("charger:new_details")

    paid_amount = info2[0]["tx"]["Amount"]
    account_from = info2[0]["tx"]["Account"]

    context = {"transactions":info2, "amount_paid": paid_amount, "balance_old" : balance_old, "balance_new": balance_new, "account_from": account_from}
    
    return render(request, "charger/show_details_new.html", context)