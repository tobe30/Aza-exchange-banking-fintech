from  django.urls import path

from account import views

app_name= "account"

urlpatterns=[
    path("", views.dashboard, name="dashboard"),
    path("account/", views.account, name="account"),
    path("kyc-reg/", views.kyc_registration, name="kyc-reg"),

    #savings
    path("savings/", views.savings_dashboard, name="savings"),
    path("add-savings/<account_number>/", views.savings_account, name="add-savings"),
    path("savings-account-process/<account_number>/", views.savings_account_process, name="add-savings-process"),
    path("savings-confirmation/<account_number>/<transaction_id>", views.SavingsConfirmation, name="savings-confirmation" ),
    path("save-process/<account_number>/<transaction_id>", views.savingprocess, name="save-process" ),
    path("save-completed/<account_number>/<transaction_id>", views.saveCompleted, name="save-completed" ),
    path("withdraw-savings/<account_number>/", views.withdraw_savingst, name="withdraw-savings"),
    path("withdraw-savings-process/<account_number>/", views.withdraw_savings_process, name="withdraw-savings-process"),
    path("withdraw-confirmation/<account_number>/<transaction_id>", views.withdrawConfirmation, name="withdraw-confirmation" ),
    path("withdraw-process/<account_number>/<transaction_id>", views.withdrawprocess, name="withdraw-process" ),
    path("withdraw-completed/<account_number>/<transaction_id>", views.withdrawCompleted, name="withdraw-completed" ),







]
