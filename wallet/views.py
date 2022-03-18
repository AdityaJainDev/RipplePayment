from multiprocessing import context
from django.shortcuts import render
from .forms import Details, PaymentDetail
import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import xrpl
from xrpl.models.transactions import Payment
from xrpl.transaction import safe_sign_transaction, send_reliable_submission
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.account import get_next_valid_seq_number
from xrpl.wallet import Wallet


# Create your views here.

def index(request):

    if request.method == 'GET':
        form = Details()
    
    elif request.method == 'POST':
        form = Details(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            # a = requests.get("https://unshorten.me/s/" + url)

            # print(a.text)

            data = requests.get(url)

            address = data.json()["address"]
            amount = data.json()["amount"]

            request.session['address'] = address
            request.session['amount'] = amount

            return redirect('wallet:payment')
    
    context = {"form": form} 

    return render(request, "base.html", context)


def payment(request):
    if request.method == 'POST':
        form = PaymentDetail(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            amount = form.cleaned_data['amount']

            print(amount)

            address_from = "rMePapujB6EfUrcgK8bUAdcyC4wRdyLNt"
            seed_1 = "sEdTum5TAn6ZDYEmJMyuugL4NCXdKza"
            seq_1 = 26106307

            testnet_url = "https://s.altnet.rippletest.net:51234"
            client = xrpl.clients.JsonRpcClient(testnet_url)

            test_wallet = Wallet(seed_1, seq_1)

            current_validated_ledger = get_latest_validated_ledger_sequence(client)
            test_wallet.sequence = get_next_valid_seq_number(address_from, client)

            my_tx_payment = Payment(
                account=address_from,
                amount=amount,
                destination=address,
                last_ledger_sequence=current_validated_ledger + 20,
                sequence=test_wallet.sequence,
                fee="10",
            )

            # sign the transaction
            my_tx_payment_signed = safe_sign_transaction(my_tx_payment,test_wallet)
            # submit the transaction
            tx_response = send_reliable_submission(my_tx_payment_signed, client)


            if str(tx_response.status) == "ResponseStatus.SUCCESS":
                request.session['address_from'] = address_from
                request.session['address_to'] = address
                request.session['amount'] = amount

                return redirect("wallet:success")
            else:
                messages.error(request, "Something went wrong, please try again")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form':form}) 
    
    return render(request, "payment.html")


def success(request):
    return render(request, "success.html")
