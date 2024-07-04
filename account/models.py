from django.db import models
from userauths.models import User
import uuid
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import  post_save


ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active")
)
EMAIL_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("not-confirmed", "Not-confirmed")
)
ID_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("not-confirmed", "Not-confirmed")
)
PHONE_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("not-confirmed", "Not-confirmed")
)
MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)



INTEREST_COMPOUNDING_CHOICES = (
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
)


# Create your models here.
def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)


class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix="217", alphabet="1234567890")
    account_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix="DEX", alphabet="1234567890")
    pin_number = ShortUUIDField(unique=True, length=4, max_length=7, alphabet="1234567890")
    ref_code = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh1234567890")
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default="in-active")
    email_status = models.CharField(max_length=100, choices=EMAIL_STATUS, default="pending")
    phone_status = models.CharField(max_length=100, choices=PHONE_STATUS, default="pending")
    id_status = models.CharField(max_length=100, choices=ID_STATUS, default="pending")
    date= models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    key_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name= "recommended_by")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"
class DollarAccount(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='dollar_account')
    dollar_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    dollar_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix="515", alphabet="1234567890")
    dollar_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix="AZA", alphabet="1234567890")
    dollar_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default="in-active")
    date= models.DateTimeField(auto_now_add=True)
    dollar_rate = models.DecimalField(max_digits=12, decimal_places=2, default=1400.00)
    
    


    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"


    

class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="kyc", default="default.jpg")
    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=10)
    gender = models.CharField(choices=GENDER, max_length=10)
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(upload_to="kyc", null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)


     #address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Contact Detail
    mobile = models.CharField(max_length=1000)
    bvn = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"    

    
    class Meta:
        ordering = ['-date']

#savings account

class SavingsAccount(models.Model):
   
    savings_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="SAVINGS")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_accounts')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Example: 2.50 for 2.5%
    interest_compounding = models.CharField(max_length=10, choices=INTEREST_COMPOUNDING_CHOICES, default='monthly')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Savings Account'
        verbose_name_plural = 'Savings Accounts'


    
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        SavingsAccount.objects.create(user=instance)
        DollarAccount.objects.create(user=instance)  # Create DollarAccount when user is created

def save_account(sender, instance, **kwargs):
    instance.account.save()

def save_savings_account(sender, instance, **kwargs):
    savings_account, created = SavingsAccount.objects.get_or_create(user=instance.user)
    if not created:
        savings_account.save()

def save_dollar_account(sender, instance, **kwargs):
    dollar_account, created = DollarAccount.objects.get_or_create(user=instance)
    if not created:
        dollar_account.save()

post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)
post_save.connect(save_dollar_account, sender=User)