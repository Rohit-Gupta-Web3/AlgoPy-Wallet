from pprint import pprint
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from algosdk.v2client import indexer
from algosdk import mnemonic, account, transaction
from algosdk.v2client import algod
from django.core.mail import send_mail
from django.contrib import messages
import qrcode
import qrcode.image.svg
from io import BytesIO

passphrase=[]

def AddAccount(request):
    holders={
        "Words1":
        {
        "word1":"Word1",
        "word2":"Word2",
        "word3":"Word3",
        "word4":"Word4",
        "word5":"Word5",
        },
         "Words2":
        {
        "word6":"Word6",
        "word7":"Word7",
        "word8":"Word8",
        "word9":"Word9",
        "word10":"Word10",
        },
         "Words3":
        {
        "word11":"Word11",
        "word12":"Word12",
        "word13":"Word13",
        "word14":"Word14",
        "word15":"Word15",
        },
         "Words4":
        {
        "word16":"Word16",
        "word17":"Word17",
        "word18":"Word18",
        "word19":"Word19",
        "word20":"Word20",
        },
         "Words5":
        {
        "word21":"Word21",
        "word22":"Word22",
        "word23":"Word23",
        "word24":"Word24",
        "word25":"Word25",
        },
    } 
    if request.method=="POST":
        p1 = request.POST.get('word1')
        p2 = request.POST.get('word2')
        p3 = request.POST.get('word3')
        p4 = request.POST.get('word4')
        p5 = request.POST.get('word5')
        p6 = request.POST.get('word6')
        p7 = request.POST.get('word7')
        p8 = request.POST.get('word8')
        p9 = request.POST.get('word9')
        p10 = request.POST.get('word10')
        p11 = request.POST.get('word11')
        p12 = request.POST.get('word12')
        p13 = request.POST.get('word13')
        p14 = request.POST.get('word14')
        p15 = request.POST.get('word15')
        p16 = request.POST.get('word16')
        p17 = request.POST.get('word17')
        p18 = request.POST.get('word18')
        p19 = request.POST.get('word19')
        p20 = request.POST.get('word20')
        p21 = request.POST.get('word21')
        p22 = request.POST.get('word22')
        p23 = request.POST.get('word23')
        p24 = request.POST.get('word24')
        p25 = request.POST.get('word25')  
        print(p10)
        passphrase = f'{p1} {p2} {p3} {p4} {p5} {p6} {p7} {p8} {p9} {p10} {p11} {p12} {p13} {p14} {p15} {p16} {p17} {p18} {p19} {p20} {p21} {p22} {p23} {p24} {p25}'
        print(passphrase)
        mnemonic_phrase = passphrase
        account_private_key = mnemonic.to_private_key(mnemonic_phrase)
        account_public_key = mnemonic.to_public_key(mnemonic_phrase)
        memo=passphrase
        privatekey=account_private_key
        address=account_public_key
        print(passphrase)
        print("your account recovered and your address is "+account_public_key + '\n'+ "and your private key is "+account_private_key)
        AddAccount.memo=passphrase
        return redirect("createRecovery")
    return render(request,"AddAccount.html",holders)



def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.method == "POST":
        name = request.POST.get('AccName')
        pwd = request.POST.get('AccPwd')          
        user = authenticate(request, username=name,password=pwd)
        if user is not None:
            login(request,user)
            current = str(request.user.username)
            print(current)
            messages.success(request, 'Your password was updated successfully!')
            return redirect("dashboard")
        else:
            return redirect("signin")          
    return render(request,"login.html")

def CreateAccount(request):
    if request.method == "POST":
        user= get_user_model()
        name=request.POST.get('AccName')
        email=request.POST.get('mail')
        pwd=request.POST.get('AccPwd')
        private_key, address = account.generate_account()
        print(name)
        add="{}".format(address)
        private="{}".format(private_key)
        pas = "{}".format(mnemonic.from_private_key(private_key))
        detail=user.objects.create_user(username=name,password=pwd,email=email,passfrase=pas,Address=add,privateKey=private)
        detail.save()
        return redirect('signin')
    return render(request, "CreateAccount.html")

@login_required(login_url="signin")
def dashboard(request):
    add=str(request.user.Address)
    name=str(request.user.username)
    algod_token = '4xcfeVtFO21zGa5oJr3us3bpzXACJjQg5oPUdTtv '
    algod_address = 'https://mainnet-algorand.api.purestake.io/ps2'
    purestake_token = {'X-Api-key': algod_token}
    algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
    account_info = algodclient.account_info(add)
    bal = "{} microAlgos".format(account_info.get('amount'))
    balance = {
        "bal" : bal,
        "add" : add,
        "name":name
    }
    return render(request, "dashboard.html", balance)

@login_required(login_url="signin")    
def SendAlgo(request):
    add=str(request.user.Address)
    algod_token = '4xcfeVtFO21zGa5oJr3us3bpzXACJjQg5oPUdTtv '
    algod_address = 'https://mainnet-algorand.api.purestake.io/ps2'
    purestake_token = {'X-Api-key': algod_token}
    algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
    account_info = algodclient.account_info(add)  
    balance=("{} microAlgos".format(account_info.get('amount')) + "\n")
    if request.method=="POST":
        sendadd = request.POST.get('Reciever')
        amt = int(request.POST.get('amount'))
        passphrase = request.POST.get('Passphrase')
        print(sendadd,amt,passphrase)
        algod_token = '4xcfeVtFO21zGa5oJr3us3bpzXACJjQg5oPUdTtv '
        algod_address = 'https://mainnet-algorand.api.purestake.io/ps2'
        purestake_token = {'X-Api-key': algod_token}
  
        #waiting for confirmation
        def wait_for_confirmation(client, txid):
            last_round = client.status().get('last-round')
            txinfo = client.pending_transaction_info(txid)
            while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
                print('Waiting for confirmation')
                last_round += 1
                client.status_after_block(last_round)
                txinfo = client.pending_transaction_info(txid)
            print('Transaction confirmed in round', txinfo.get('confirmed-round'))
            return txinfo

        #Sending Algo from one account to another
        mnemonic_phrase = passphrase
        account_private_key = mnemonic.to_private_key(mnemonic_phrase)
        account_public_key = mnemonic.to_public_key(mnemonic_phrase)
        print("My address: {}".format(account_public_key))
        algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
        params = algodclient.suggested_params()
        gh = params.gh
        first_valid_round = params.first
        last_valid_round = params.last
        fee = params.min_fee
        send_amount = amt
        print(account_public_key)
        existing_account = account_public_key
        send_to_address = sendadd
        tx = transaction.PaymentTxn(existing_account, fee, first_valid_round, last_valid_round, gh, send_to_address, send_amount, flat_fee=True)
        signed_tx = tx.sign(account_private_key)
        tx_confirm = algodclient.send_transaction(signed_tx)
        print('Transaction sent with ID', signed_tx.transaction.get_txid())
        wait_for_confirmation(algodclient, txid=signed_tx.transaction.get_txid())
        account_info = algodclient.account_info(account_public_key)  
        print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
    return render(request, "send.html",{'balance':balance})

@login_required(login_url="signin")
def RecieveAlgo(request):
    add=str(request.user.Address)
    name=str(request.user.username)

    algod_token = '4xcfeVtFO21zGa5oJr3us3bpzXACJjQg5oPUdTtv '
    algod_address = 'https://mainnet-algorand.api.purestake.io/ps2'
    purestake_token = {'X-Api-key': algod_token}
    algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
    account_info = algodclient.account_info(add)
    bal = "{} microAlgos".format(account_info.get('amount'))
    print(bal)
    print(name)
    context = {"address":add}
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make((add), image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    context["svg"] = stream.getvalue().decode()
    
    return render(request, "recieve.html",context=context)
@login_required(login_url="signin")
def History(request):
    owner=str(request.user.Address)
    algod_token = '4xcfeVtFO21zGa5oJr3us3bpzXACJjQg5oPUdTtv'
    algod_address = 'https://mainnet-algorand.api.purestake.io/idx2'
    purestake_token = {'X-API-Key': algod_token}
    acl = indexer.IndexerClient(algod_token, algod_address,headers=purestake_token)
    response = acl.search_transactions(address=owner)
    amt=(response["transactions"])
    kampy=[]
    sno=0
    for amt in amt:
        id=amt["id"]
        cnfround=amt["confirmed-round"]
        amount=amt["payment-transaction"]["amount"]
        sender=amt["sender"]
        receiver=amt["payment-transaction"]["receiver"]
        fee=amt["fee"]
        if sender==owner:
            tnxtype="Sent"
        else:
            tnxtype="Receive"
        sno=sno+1
        divyansh= {"sno":sno,"id":id,"cnfround":cnfround,"amount":amount,"receiver":receiver,"sender":sender ,"fee":fee,"tnxtype":tnxtype}
        kampy.append(divyansh)
    return render(request,'history.html',{'divyansh':kampy})

def createRecovery(request):
    if request.method=="POST":
        passphrase=AddAccount.memo
        mnemonic_phrase = passphrase
        account_private_key = mnemonic.to_private_key(mnemonic_phrase)
        account_public_key = mnemonic.to_public_key(mnemonic_phrase)
        user= get_user_model()
        username = request.POST.get('AccName')
        email = request.POST.get('mail')
        pwd = request.POST.get('AccPwd')
        print(username)
        detail=user.objects.create_user(username=username,password=pwd,email=email,passfrase=passphrase,Address=account_public_key,privateKey=account_private_key)
        detail.save()
        current = str(request.user)
        print(current)
        return redirect('signin')
    return render(request, "createRecovery.html")

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        
    return redirect('signin')

def sendmail(request):
    if request.method=="POST":
        add=str(request.user.Address)
        name=str(request.user.username)
        private=str(request.user.privateKey)
        pas=str(request.user.passfrase)
        email=str(request.user.email)
        algod_token = '4xcfeVtFO21zGa5oJr3us3bpzXACJjQg5oPUdTtv '
        algod_address = 'https://mainnet-algorand.api.purestake.io/ps2'
        purestake_token = {'X-Api-key': algod_token}
        algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
        account_info = algodclient.account_info(add)
        bal = "{} microAlgos".format(account_info.get('amount'))
        balance = {
            "bal" : bal,
            "add" : add,
            "name":name
        }
        subject="Algopy Account details of "+ name
        data="Hello " + name + "\n"+"Your Account Address is : " + add + "\n"+"your Account private key is : "+ private +"\n"+"and your Passphrase is : " + pas + "\n" +"Thankyou for choosing Algopy \n Team Algopy."
        send_mail(
                subject,
                data,
                'AlgoPy.wallet@gmail.com',
                [email],
            )
    return render(request, "dashboard.html",balance)
