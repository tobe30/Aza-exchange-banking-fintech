from account.models import KYC, Account
from core.models import Notification

def default(request):
    if not request.user.is_authenticated:
        return {}

    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        kyc = None

    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        account = None
        
    try:
        notifications = Notification.objects.filter(user=request.user).order_by("-id")[:10]
    except:
        notifications = None


    return {
        "kyc": kyc,
        "account": account,
        "notifications":notifications,
        
    }
