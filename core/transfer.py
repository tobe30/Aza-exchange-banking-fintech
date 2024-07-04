from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account, KYC, DollarAccount
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction, Notification, Recipient
from decimal import Decimal
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
def pay(request):
    
    return render(request, "transfer/pay.html")

@login_required
def search_users(request): 
    account = Account.objects.all()
    query=request.POST.get("account_number")
    recipients = Recipient.objects.filter(user=request.user).select_related('user__kyc')
    

    if query:
        account = account.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct()

    context ={
        "account":account,
        "query":query,
        "recipients":recipients,
    }
    return render(request, "transfer/search-user-by-account-number.html", context)

def recipient(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    recipients = Recipient.objects.filter(user=request.user).select_related('user__kyc')
    
    context = {
        "recipient": recipients
    }
    return render(request, "transfer/recipient.html", context)
    
@login_required
def search_dollarusers(request):
    account = DollarAccount.objects.all()
    query=request.POST.get("account_number")
    recipients = Recipient.objects.filter(user=request.user).select_related('user__kyc')

    if query:
        account = account.filter(
            Q(dollar_number=query)|
            Q(dollar_id=query)
        ).distinct()

    context ={
        "account":account,
        "query":query,
         "recipients":recipients,
    }
    return render(request, "transfer/search-user-by-dollar-number.html", context)

@login_required
def AmountTransfer(request, account_number):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
    try:
        account= Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, "Account does not exist")
        return redirect("core:search-account")


    context ={
        "account":account,
    }
    return render(request, "transfer/amount-transfer.html", context)


@login_required
def AmountDollarTransfer(request, dollar_number):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
    try:
        account= DollarAccount.objects.get(dollar_number=dollar_number)
    except:
        messages.warning(request, "Account does not exist")
        return redirect("core:search-account")


    context ={
        "account":account,
    }
    return render(request, "transfer/amount-dollar-transfer.html", context)

@login_required
def AmountTransferProcess(request, account_number):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        account = Account.objects.get(account_number=account_number)##get the account that the money will be sent to
        sender = request.user #the person that is loggin
        reciever = account.user #the person that is going to recieve the money

        sender_account = request.user.account #get the currently logged in users account that would send the money
        reciever_account = account #get the person account that would recieve the money

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        print(amount)
        print(description)

        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                reciever=reciever,
                sender=sender,
                sender_account=sender_account,
                reciever_account=reciever_account,
                status = "processing",
                transaction_type="transfer",
                currency = "NGN"  # Set the currency as USD for this example
            )
            new_transaction.save()

            #get the id of the transaction that was created now
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "insufficient fund")
            return redirect("core:amount-transfer", account.account_number)
    else:
        messages.warning(request, "Error occured try again later")
        return redirect("acccount:account")
    
@login_required
def AmountDollarProcess(request, dollar_number):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        account = DollarAccount.objects.get(dollar_number=dollar_number)##get the account that the money will be sent to
        sender = request.user #the person that is loggin
        reciever = account.user #the person that is going to recieve the money

        sender_account = request.user.dollar_account #get the currently logged in users account that would send the money
        reciever_account = account #get the person account that would recieve the money

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        print(amount)
        print(description)

        if sender_account.dollar_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                reciever=reciever,
                sender=sender,
                sender_dollar_account=sender_account,
                reciever_dollar_account=reciever_account,
                status = "processing",
                transaction_type="transfer",
                currency = "USD"  # Set the currency as USD for this example
                
            )
            new_transaction.save()

            #get the id of the transaction that was created now
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-dollar-confirm", account.dollar_number, transaction_id)
        else:
            messages.warning(request, "insufficient fund")
            return redirect("core:amount-dollar-transfer", account.dollar_number)
    else:
        messages.warning(request, "Error occured try again later")
        return redirect("acccount:account")

@login_required  
def TransferDollarConfirm(request, dollar_number, transaction_id):
    try:
        account = DollarAccount.objects.get(dollar_number=dollar_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transaction does not exist ")
            return redirect("core:amount-transfer", account.dollar_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "transfer/transfer-dollar-confirm.html", context)

@login_required  
def TransferConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transaction does not exist ")
            return redirect("core:amount-transfer", account.account_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "transfer/transfer-confirmation.html", context)


@login_required
def TransferDollarProcess(request, dollar_number, transaction_id):
    account = DollarAccount.objects.get(dollar_number=dollar_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    kyc = KYC.objects.get(user=account.user)
    full_name = kyc.full_name
    
    sender_acc = Account.objects.get(user=request.user)

    sender = request.user 
    receiver = account.user 
    receiver_kyc = get_object_or_404(KYC, user=receiver)
    

    sender_account = request.user.dollar_account 
    receiver_account = account

    completed = False
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        print(pin_number)

        if pin_number == sender_acc.pin_number:
            transaction.status = "completed"
            transaction.save()

            # Remove the amount that am sending from my account balance and update my amount
            sender_account.dollar_balance -= transaction.amount
            sender_account.save()

            # Add the amount that was removed from my account to the person that i am sending the money to
            account.dollar_balance += transaction.amount
            account.save()
            
            account_type = "USD"  
            # Recipient create or get
            recipient, created = Recipient.objects.get_or_create(
                kyc=receiver_kyc,
                account_type=account_type,
                defaults={
                    'r_number': account.dollar_number,
                    'user': sender,
                    'full_name': full_name,
                    'account_type': 'USD'
                }
            )
            
            if not created:
                recipient.r_number = account.dollar_number
                recipient.user = sender
                recipient.full_name = full_name
                recipient.account_type = 'USD'
                recipient.save()
            
            # Create Notification Object
            Notification.objects.create(
                amount=transaction.amount,
                user=account.user,
                notification_type="Credit Alert",
                currency="USD"
            )
            
            Notification.objects.create(
                user=sender,
                notification_type="Debit Alert",
                amount=transaction.amount,
                currency="USD"
            )

            messages.success(request, "Transfer successful.")
            return redirect("core:transfer-dollar-completed", account.dollar_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect('core:transfer-dollar-confirmation', account.dollar_number, transaction.transaction_id)
    else:
        messages.warning(request, "An error occurred. Try again later.")
        return redirect('account:dashboard')


@login_required
def TransferProcess(request, account_number, transaction_id):

    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    kyc = KYC.objects.get(user=account.user)
    full_name = kyc.full_name

    sender = request.user 
    reciever = account.user 
    receiver_kyc = get_object_or_404(KYC, user=reciever)

    sender_account = request.user.account 
    reciever_account = account

    completed = False
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        print(pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            #remove the amount that am sending from my account balance and update my amount
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            # Add the amount that was removed from my account to the person that i am sending the money to recipient_list_sender = [sender.email]
            account.account_balance += transaction.amount
            account.save()
            
            account_type = "NGN"  
            #recipient create
            
            recipient, created = Recipient.objects.get_or_create(
                kyc=receiver_kyc,
                account_type=account_type,
                defaults={
                    'r_number': account.account_number,
                    'user': sender,
                    'full_name': full_name,
                    'account_type': 'NGN'
                }
            )
            
            if not created:
                recipient.r_number = account.account_number
                recipient.user = sender
                recipient.full_name = full_name
                recipient.account_type = 'NGN'
                recipient.save()
            
                
                  
            
             # Create Notification Object
            Notification.objects.create(
                amount=transaction.amount,
                user=account.user,
                notification_type="Credit Alert",
                currency = "NGN"
                
            )
            
            Notification.objects.create(
                user=sender,
                notification_type="Debit Alert",
                amount=transaction.amount,
                currency = "NGN"
                
            )

            messages.success(request, "Transfer successfull.")
            return redirect("core:transfer-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect('core:transfer-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An error occured try again later")
        return redirect('account:dashboard')

@login_required   
def TransferCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transfer does not exist ")
            return redirect("core:amount-transfer", account.account_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "transfer/transfer-completed.html", context)

@login_required   
def TransferDollarCompleted(request, dollar_number, transaction_id):
    try:
        account = DollarAccount.objects.get(dollar_number=dollar_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transfer does not exist ")
            return redirect("core:amount-dollar-transfer", account.dollar_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "transfer/transfer-dollar-completed.html", context)