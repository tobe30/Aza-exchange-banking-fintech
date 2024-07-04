from django.contrib import admin
from account.models import Account, KYC, SavingsAccount, DollarAccount
from userauths.models import User
from import_export.admin  import ImportExportModelAdmin

# Register your models here.

class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'account_balance'] 
    list_display = ['user', 'account_number' ,'account_status', 'account_balance'] 
    list_filter = ['account_status']

class DollarAccountAdmin(ImportExportModelAdmin):
    list_editable = ['dollar_status', 'dollar_balance', 'dollar_rate'] 
    list_display = ['user', 'dollar_number' ,'dollar_status', 'dollar_balance', 'dollar_rate'] 
    list_filter = ['dollar_status']


class KYCAdmin(ImportExportModelAdmin):
    search_fields = ["full_name"]
    list_display = ['user', 'full_name'] 

class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'interest_rate', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('interest_compounding', 'created_at')

admin.site.register(Account, AccountAdminModel)
admin.site.register(DollarAccount, DollarAccountAdmin)
admin.site.register(KYC, KYCAdmin)
admin.site.register(SavingsAccount, SavingsAccountAdmin)