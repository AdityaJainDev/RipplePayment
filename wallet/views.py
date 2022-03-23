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

address_from = "r3YrQpHhvCviAxgzFKtqqBVNtXB3ecAb9Q"
seed_1 = "sEd7g3sjDmyUisSoRER9cCj4WpzVsfC"
seq_1 = 26299123

testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

def index(request):

    if request.method == 'GET':                    
        form = Details()
    
    elif request.method == 'POST':
        form = Details(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            import requests

            resp = requests.get("https://tinyurl.com/" + url)

            data = requests.get(resp.url)

            address = data.json()["address"]
            amount = data.json()["amount"]

            request.session['address'] = address
            request.session['amount'] = amount

            return redirect('wallet:payment')
    
    context = {"form": form} 

    return render(request, "base.html", context)


def generate_wallet(request):
    return render(request, "generate_wallet.html")

def generate_wallet_car(request):

    from xrpl.wallet import generate_faucet_wallet, Wallet
    test_wallet = generate_faucet_wallet(client, debug=True)

    info1 = xrpl.account.get_balance(test_wallet.classic_address, client)

    request.session['new_address_car'] = test_wallet.classic_address
    request.session['new_address_seed'] = test_wallet.seed
    request.session['new_sequence'] = test_wallet.sequence
    request.session['new_balance'] = info1

    return render(request, "generate_wallet_car.html")


def payment(request):
    if request.method == 'POST':
        form = PaymentDetail(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            amount = form.cleaned_data['amount']

            testnet_url = "https://s.altnet.rippletest.net:51234"
            client = xrpl.clients.JsonRpcClient(testnet_url)

            if request.session['new_address_seed'] != "":
                seed_1 = request.session['new_address_seed']
                seq_1 = request.session['new_sequence']
                address_from = request.session['new_address_car']

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

def transactions(request):

    if request.session['new_address_seed'] != "":
        address_from = request.session['new_address_car']
    
    info2 = xrpl.account.get_account_payment_transactions(address_from, client)
    info1 = xrpl.account.get_balance(address_from, client)

    context = {"transactions":info2, "balance": info1}
    
    return render(request, "transactions.html", context)
