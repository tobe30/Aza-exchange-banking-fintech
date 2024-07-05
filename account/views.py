from django.shortcuts import render, redirect, get_object_or_404
from account.models import KYC, Account, SavingsAccount, DollarAccount
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Transaction, CreditCard, Notification
from decimal import Decimal

# Create your views here.
@login_required
def dashboard(request):

    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        
        sender_transaction = Transaction.objects.filter(sender=request.user).order_by("-id")[:5]
        reciever_transaction = Transaction.objects.filter(reciever=request.user).order_by("-id")[:5]

        request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")[:5]
        request_reciever_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request")[:5]
        
        account = Account.objects.get(user=request.user)
        dollar_account = DollarAccount.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by("-id")


    context = {
        "kyc":kyc,
        "account":account,
        "dollar_account":dollar_account,
        "sender_transaction":sender_transaction,
        "reciever_transaction":reciever_transaction,

        'request_sender_transaction':request_sender_transaction,
        'request_reciever_transaction':request_reciever_transaction,
        'credit_card':credit_card
    }
    return render(request, "account/dashboard.html", context)

@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)
    dollaraccount = DollarAccount.objects.get(user=user)
    
    try:
        kyc = KYC.objects.get(user=user)
    except KYC.DoesNotExist:
        kyc = None
    
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.save()

            # Update the account status to active
            account.account_status = "active"
            account.kyc_submitted = True  # Set kyc_submitted to True upon form submission    
            account.save()
            
            # Update the dollar account status
            dollaraccount.dollar_status = "active"
            dollaraccount.save()
            
            messages.success(request, "KYC Form submitted successfully, In review now.")
            return redirect("account:dashboard")
    else:
        form = KYCForm(instance=kyc)
    
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    
    return render(request, "account/kyc-form.html", context)


@login_required
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("userauths:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
    }
    return render(request, "account/account.html", context)

@login_required
def savings_dashboard(request):

    save_transaction = Transaction.objects.filter(user=request.user, transaction_type="save").order_by("-id")
    withdraw_transaction = Transaction.objects.filter(user=request.user, transaction_type="withdraw").order_by("-id")


    
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        
        account = Account.objects.get(user=request.user)
        savings_account = SavingsAccount.objects.get(user=request.user)

        context ={
            "account":account,
            "savings_account":savings_account,
            "save_transaction":save_transaction,
            "withdraw_transaction":withdraw_transaction,

        }

        return render(request, "account/savings_account.html", context)

@login_required
def savings_account(request, account_number):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        
    try:
        account= Account.objects.get(account_number=account_number, user=request.user)
    except:
        messages.warning(request, "Access Denied")
        return redirect("account:savings")
   

    context ={
        "account":account,
    }
    return render(request, "account/add-savings.html", context)

@login_required
def savings_account_process(request, account_number):
    account = get_object_or_404(Account, account_number=account_number, user=request.user)
    savings_account, created = SavingsAccount.objects.get_or_create(user=account.user)
    sender_account = request.user.account 

    if request.method == "POST":
        amount = request.POST.get("amount-save")

        if sender_account.account_balance >= Decimal(amount):

         new_savings = Transaction.objects.create(
            user=request.user,
            amount = amount,
            status = "processing",
            transaction_type = "save"
        )
         new_savings.save()

        #get the id of the transaction that was created now
         transaction_id = new_savings.transaction_id
         return redirect("account:savings-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "insufficient fund")
            return redirect("account:add-savings", account.account_number)
        
    else:
        messages.warning(request, "Error occured try again later")
        return redirect("acccount:account")
    
@login_required 
def SavingsConfirmation(request, account_number, transaction_id):

    try:
        account = Account.objects.get(account_number=account_number, user=request.user)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transaction does not exist ")
            return redirect("account:add-savings", account.account_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "account/savings-confirmation.html", context)

@login_required 
def savingprocess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number, user=request.user)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    savings_account, created = SavingsAccount.objects.get_or_create(user=account.user)

    sender_account = request.user.account 

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")

        if pin_number == sender_account.pin_number:
            transaction.status= "completed"
            transaction.save()

            sender_account.account_balance -= transaction.amount
            sender_account.save()

            savings_account.balance += transaction.amount
            savings_account.save()  # Ensure to save the savings account
            
            Notification.objects.create(
                amount=transaction.amount,
                user=account.user,
                notification_type="Saved Funds"
            )

            messages.success(request, "Saved successfully")
            return redirect("account:save-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect('account:savings-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An error occured try again later")
        return redirect('account:dashboard')
    
@login_required
def saveCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number, user=request.user)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transfer does not exist ")
            return redirect("account:add-savings", account.account_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "account/save-completed.html", context)


@login_required
def withdraw_savingst(request, account_number):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        
    try:
        account= Account.objects.get(account_number=account_number, user=request.user)
    except:
        messages.warning(request, "Access Denied")
        return redirect("account:savings")
   

    context ={
        "account":account,
    }
    return render(request, "account/withdraw-savings.html", context)


@login_required
def withdraw_savings_process(request, account_number):
    account = get_object_or_404(Account, account_number=account_number, user=request.user)
    savings_account, created = SavingsAccount.objects.get_or_create(user=account.user)
    sender_account = request.user.account 

    if request.method == "POST":
        amount = request.POST.get("amount-save")

        if savings_account.balance >= Decimal(amount):

         new_savings = Transaction.objects.create(
            user=request.user,
            amount = amount,
            status = "processing",
            transaction_type = "withdraw"
        )
         new_savings.save()

        #get the id of the transaction that was created now
         transaction_id = new_savings.transaction_id
         return redirect("account:withdraw-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "insufficient fund")
            return redirect("account:withdraw-savings", account.account_number)
        
    else:
        messages.warning(request, "Error occured try again later")
        return redirect("acccount:account")
    
@login_required 
def withdrawConfirmation(request, account_number, transaction_id):

    try:
        account = Account.objects.get(account_number=account_number, user=request.user)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transaction does not exist ")
            return redirect("account:withdraw-savings", account.account_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "account/withdraw-confirmation.html", context)


@login_required 
def withdrawprocess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number, user=request.user)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    savings_account, created = SavingsAccount.objects.get_or_create(user=account.user)

    sender_account = request.user.account 

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")

        if pin_number == sender_account.pin_number:
            transaction.status= "completed"
            transaction.save()


            savings_account.balance -= transaction.amount
            savings_account.save()  # Ensure to save the savings account

            sender_account.account_balance += transaction.amount
            sender_account.save()

            messages.success(request, "Withdawn successfully")
            return redirect("account:withdraw-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect('account:withdraw-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An error occured try again later")
        return redirect('account:dashboard')
    

@login_required
def withdrawCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
            messages.warning(request, "Transfer does not exist ")
            return redirect("account:add-savings", account.account_number)
    context={
        "account":account,
        "transaction":transaction,
    }
    return render(request, "account/withdraw-completed.html", context)