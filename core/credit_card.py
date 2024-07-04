# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import CreditCard, Notification
from .utils import generate_random_credit_card
from account.models import  Account, KYC
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()



@login_required
def process_payment(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        if amount == 5000:
            try:
                account = Account.objects.get(user=request.user)
                admin_user = User.objects.get(username='tobe')  # Assuming 'admin' is the username of your admin user
                admin_account = Account.objects.get(user=admin_user)

                if account.account_balance >= Decimal(amount):
                    # Simulate a successful payment for this example
                    # Deduct the amount from the user's account balance
                    account.account_balance -= Decimal(amount)
                    admin_account.account_balance -= 5000
                    account.save()
                    
                    

                    # Generate random credit card details
                    card_details = generate_random_credit_card()
                    # Retrieve the full name from the KYC model
                    try:
                        kyc = KYC.objects.get(user=request.user)
                        full_name = kyc.full_name
                    except KYC.DoesNotExist:
                        messages.warning(request, "You need to submit your kyc")
                        return redirect("account:kyc-reg")

                    # Create a new credit card for the user
                    CreditCard.objects.create(
                        user=request.user,
                        name=full_name,  # Use the full name from the KYC model
                        number=card_details['number'],
                        month=card_details['month'],
                        year=card_details['year'],
                        cvv=card_details['cvv'],
                        card_type=card_details['card_type']
                    )

                    # Add 5000 to the admin's account balance
                    admin_account.account_balance += 5000
                    admin_account.save()
                    
                    Notification.objects.create(
                    user=request.user,
                    amount=amount,
                    notification_type="Added Credit Card"
                )

                    messages.warning(request, "Card purchased successfully")
                    return redirect("account:dashboard")  # Redirect to a success page or similar
                else:
                    messages.warning(request, "insufficient fund")
                    return redirect("account:dashboard")
            except Account.DoesNotExist:
                messages.warning(request, "Account not fount")
                return redirect("account:dashboard")
            except User.DoesNotExist:
                messages.warning(request, "Admin user not found")
                return redirect("account:dashboard")

        else:
            # Handle case where payment amount is incorrect
            messages.warning(request, "incorrect amount")
            return redirect("account:dashboard")

    return render(request, 'account/dashboard.html')


def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credic_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        "account":account,
        "credic_card":credic_card,
    }
    return render(request, "creditcard/card-detail.html", context)

def fund_credit_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account
    
    if request.method == "POST":
        amount = request.POST.get("funding_amount") # 25
        
        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount) ## 14,790.00 - 20
            account.save()
            
            credit_card.amount += Decimal(amount)
            credit_card.save()
            
            Notification.objects.create(
                amount=amount,
                user=request.user,
                notification_type="Funded Credit Card"
            )
            
           
            messages.success(request, "Funding Successfull")
            return redirect("core:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)
        
def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        print(amount)

        if credit_card.amount >= Decimal(amount) and credit_card.amount != 0.00:
            account.account_balance += Decimal(amount)
            account.save()

            credit_card.amount -= Decimal(amount)
            credit_card.save()
            
            Notification.objects.create(
                user=request.user,
                amount=amount,
                notification_type="Withdrew Credit Card Funds"
            )
            
            

            messages.success(request, "Withdrawal Successfull")
            return redirect("core:card-detail", credit_card.card_id)
        elif credit_card.amount == 0.00:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:card-detail", credit_card.card_id)

def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    
    # New Feature
    # BEfore deleting card, it'll be nice to transfer all the money from the card to the main account balance.
    account = request.user.account
    
    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()
        
        Notification.objects.create(
            user=request.user,
            notification_type="Deleted Credit Card"
        )
        
        
        credit_card.delete()
        messages.success(request, "Card Deleted Successfull")
        return redirect("account:dashboard")
    
    Notification.objects.create(
        user=request.user,
        notification_type="Deleted Credit Card"
    )
   
    
    credit_card.delete()
    messages.success(request, "Card Deleted Successfull")
    return redirect("account:dashboard")