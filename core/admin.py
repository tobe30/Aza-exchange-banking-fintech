from django.contrib import admin


# Register your models here.
from django.contrib import admin
from core.models import Transaction, CreditCard, Notification, Recipient
# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'amount_exchange', 'status', 'transaction_type']
    list_display = ['user', 'amount', 'amount_exchange', 'status', 'transaction_type', 'reciever', 'sender', 'currency']

class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type']
    list_display = ['user', 'amount',  'card_type']
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'amount' ,'date', 'currency']
    
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'r_number']

admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Recipient, RecipientAdmin)




