from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from core.models import Transaction, Notification

@login_required
def SearchUsersRequest(request):
    accounts = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        accounts = accounts.filter(Q(account_number__icontains=query)).distinct()

    context = {
        "accounts":accounts,
        "query":query
    }
    return render(request, "payment_request/search-users.html", context)

@login_required
def AmountRequest(request, account_number):
     try:
         account = Account.objects.get(account_number=account_number)
     except:
            messages.warning(request, "Account does not exist")
            return redirect("core:request-search-account")
     context = {
        "account": account,
    }
     return render(request, "payment_request/amount-request.html", context)

@login_required
def AmountRequestProcess(request, account_number):
    account = Account.objects.get(account_number=account_number)

    sender = request.user
    reciever = account.user

    sender_account = request.user.account
    reciever_account = account 

    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")

        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,

            sender=sender,
            reciever=reciever,

            sender_account=sender_account,
            reciever_account=reciever_account,
 
            status="request_processing",
            transaction_type="request"
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "Error Occured, try again later.")
        return redirect("account:dashboard")
    
@login_required
def AmountRequestConfirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account":account,
        "transaction":transaction,
    }
    return render(request, "payment_request/amount-request-confirmation.html", context)

@login_required
def AmountRequestFinalProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method=="POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            transaction.status = "request_sent"
            transaction.save()
            
            Notification.objects.create(
                user=account.user,
                notification_type="Recieved Payment Request",
                amount=transaction.amount,
                
            )
            
            Notification.objects.create(
                user=request.user,
                amount=transaction.amount,
                notification_type="Sent Payment Request"
            )

            messages.success(request, "Your payment request has been sent successfully")
            return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect('core:amount-request-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An error occurred, try again later")
        return messages("account:dashboard")
    
@login_required
def RequestCompleted(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/amount-request-completed.html", context)

##################### settled ####################
@login_required
def settlement_confirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/settlement-confirmation.html", context)
@login_required


def settlement_processing(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except (Account.DoesNotExist, Transaction.DoesNotExist):
        messages.error(request, "Account or transaction not found.")
        return redirect("account:dashboard")

    sender = request.user
    sender_account = sender.account

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == sender_account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request, "Insufficient Funds, fund your account and try again.")
                return redirect("core:settlement-confirmation", account.account_number, transaction.transaction_id)
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.status = "request_settled"
                transaction.save()

                messages.success(request, f"Settlement to {account.user.kyc.full_name} was successful.")
                return redirect("core:settlement-completed", account.account_number, transaction.transaction_id)

        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("core:settlement-confirmation", account.account_number, transaction.transaction_id)

    # Fallback for non-POST requests or unexpected scenarios
    messages.warning(request, "Error Occurred")
    return redirect("account:dashboard")


@login_required   
def SettlementCompleted(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/settlement-completed.html", context)

@login_required
def deletepaymentrequest(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.user == transaction.user:
        transaction.delete()
        messages.success(request, "Payment Request Deleted Sucessfully")
        return redirect("core:transactions")
    else:
        messages.warning(request, "Something went Wrong try again Later")
        return redirect("core:transactions")
    
@login_required
def deleterecieverequest(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    
    transaction.delete()
    messages.success(request, "Cancelled request successfully")
    return redirect("core:transactions")
