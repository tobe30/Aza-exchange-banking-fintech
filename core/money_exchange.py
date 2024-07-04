from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import Account, KYC, DollarAccount
from decimal import Decimal, InvalidOperation
from core.models import Transaction, Notification
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def money_exchange(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except KYC.DoesNotExist:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
    try:
        dollar_account = DollarAccount.objects.get(user=request.user)
    except DollarAccount.DoesNotExist:
        messages.warning(request, "Account does not exist")
        return redirect("core:search-account")

    context = {
        "dollar_account": dollar_account,
    }

    return render(request, "exchange/money-exchange.html", context)

@login_required
def DollarTransferProcess(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except KYC.DoesNotExist:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")

        sender = request.user
        # Get the sender's Account
        sender_account = Account.objects.get(user=request.user)
        # Get the sender's DollarAccount
        sender_dollar_account = DollarAccount.objects.get(user=request.user)
        # Get the receiver's DollarAccount hidden-estimated-fee
        

    if request.method == "POST":
        dollar_amount_str = request.POST.get("hidden-total-to-pay")
        exchange_amount_str = request.POST.get("recipient-gets")
        amount_fee = request.POST.get("hidden-estimated-fee")



        try:
            dollar_amount = Decimal(dollar_amount_str)
            amount_exchange = Decimal(exchange_amount_str)
            amount_fee = Decimal(amount_fee)


        except (InvalidOperation, TypeError, ValueError):
            messages.warning(request, "Invalid amount")
            return redirect("core:money_exchange")

        if sender_dollar_account.dollar_balance >= dollar_amount:
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=dollar_amount,
                amount_exchange=amount_exchange,
                amount_fee =amount_fee,
                sender=sender,
                currency = "USD",     
                sender_account=sender_account,
                sender_dollar_account=sender_dollar_account, # Correct field for sender's DollarAccount
                transaction_type="transfer"
            )
            new_transaction.save()

            transaction_id = new_transaction.transaction_id
            return redirect("core:exchange-confirmation", sender_dollar_account.dollar_number, transaction_id)
        else:
            messages.warning(request, "Insufficient funds")
            return redirect("core:money_exchange")

    else:
        messages.warning(request, "Error occurred, try again later")
        return redirect("core:money_exchange")

@login_required    
def exchangeconfirmation(request, dollar_number, transaction_id):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except KYC.DoesNotExist:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
    try:
        dollar_account = DollarAccount.objects.get(dollar_number=dollar_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        adjusted_amount = transaction.amount - transaction.amount_fee

    except (DollarAccount.DoesNotExist, Transaction.DoesNotExist):
        messages.warning(request, "Transaction does not exist or you do not have a dollar account.")
        return redirect("core:money_exchange")

    if request.method == "POST":
        account_number = request.POST.get("accountnumber")
        sending_reason = request.POST.get("sendingreason")

        try:
            account = Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            messages.warning(request, "Account number does not exist.")
            context = {
                "dollar_account": dollar_account,
                "transaction": transaction,
                "adjusted_amount": adjusted_amount,
            }
            return render(request, "exchange/exchange-confirmation.html", context)
        
        reciever = account.user
        
        print("Receiver:", reciever)  # Debug statement

        transaction.description = sending_reason
        transaction.reciever = reciever  # Assign the receiver correctly
        transaction.status="processing"
        transaction.currency = "NGN"
        transaction.save()

        print("Transaction after save:", transaction.reciever)  # Debug statement


        return redirect("core:exchange-confirmrate", dollar_number=dollar_account.dollar_number, account_number=account_number, transaction_id=transaction_id)

    context = {
        "dollar_account": dollar_account,
        "transaction": transaction,
        "adjusted_amount": adjusted_amount,
    }
    return render(request, "exchange/exchange-confirmation.html", context)

def check_kyc(request):
    if request.user.is_authenticated:
        try:
            KYC.objects.get(user=request.user)
        except KYC.DoesNotExist:
            messages.warning(request, "You need to submit your KYC")
            return False
    return True

@login_required
def exchangeconfirmrate(request, dollar_number, account_number, transaction_id):

    if not check_kyc(request):
        return redirect("account:kyc-reg")

    try:
        dollar_account = DollarAccount.objects.get(dollar_number=dollar_number)
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        adjusted_amount = transaction.amount - transaction.amount_fee
    except (DollarAccount.DoesNotExist, Transaction.DoesNotExist):
        messages.warning(request, "Transaction does not exist or you do not have a dollar account.")
        return redirect("core:money_exchange")
    
    context = {
        "dollar_account": dollar_account,
        "transaction": transaction,
        "adjusted_amount": adjusted_amount,
        "account":account
    }
    return render(request, "exchange/exchange-confirmrate.html", context)

@login_required
def exchangerateprocess(request, dollar_number, account_number, transaction_id):

    if not check_kyc(request):
        return redirect("account:kyc-reg")

    dollar_account = DollarAccount.objects.get(dollar_number=dollar_number)
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user
    reciever= request.user
    

    sender_account = request.user.dollar_account 
    reciever_account = account
    pin_account = request.user.account 
    

    completed = False
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        print(pin_number)

        if pin_number == pin_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            #remove the amount that am sending from my account balance and update my amount
            sender_account.dollar_balance -= transaction.amount
            sender_account.save()

             # Add the amount that was removed from my account to the person that i am sending the money to
            account.account_balance += transaction.amount_exchange
            account.save()
            
            # Fetch admin user (assuming admin is a superuser)
            admin_user = User.objects.get(is_superuser=True)

                # Add fee to admin's DollarAccount
            admin_dollar_account = DollarAccount.objects.get(user=admin_user)
            admin_dollar_account.dollar_balance = F('dollar_balance') + transaction.amount_fee
            admin_dollar_account.save()
            
            # Create Notification Object
            Notification.objects.create(
                amount=transaction.amount_exchange,
                user=account.user,
                notification_type="Credit Alert",
                currency="NGN"
            )
            
            Notification.objects.create(
                user=sender,
                notification_type="Debit Alert",
                amount=transaction.amount,
                currency="USD"
                
            )

            messages.success(request, "Transfer successfull.")
            return redirect("core:exchange-completed", dollar_number=dollar_account.dollar_number, account_number=account_number, transaction_id=transaction_id)

        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("core:exchange-confirmrate", dollar_number=dollar_account.dollar_number, account_number=account_number, transaction_id=transaction_id)
    else:
        messages.warning(request, "An error occured try again later")
        return redirect('account:dashboard')

@login_required
def ExchangeCompleted(request, dollar_number, account_number, transaction_id):
    try:
       dollar_account = DollarAccount.objects.get(dollar_number=dollar_number)
       account = Account.objects.get(account_number=account_number)
       transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transfer does not exist ")
            return redirect("core:money_exchange")
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "exchange/exchange-completed.html", context)