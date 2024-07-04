from django.urls import path
from core import views, transfer, transaction, payment_request, credit_card, money_exchange

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("coming-soon/", views.comingsoon, name="coming-soon"),
    path("about-us/", views.aboutus, name="about-us"),
    
 
    
    #emails
    path("reg_email/", views.new_useremail, name="reg_email"),
    path("trans_email/", views.trans_email, name="trans_email"),

    
    


    #transfers
    path("search-account/", transfer.search_users, name="search-account" ),
    path("pay/", transfer.pay, name="pay" ),
    path("recipient/", transfer.recipient, name="recipient" ),

    
    path("search-dollar-account/", transfer.search_dollarusers, name="search-dollar-account" ),
    path("amount-transfer/<account_number>/", transfer.AmountTransfer, name="amount-transfer" ),
    path("amount-dollar-transfer/<dollar_number>/", transfer.AmountDollarTransfer, name="amount-dollar-transfer" ),
    path("amount-dollar-process/<dollar_number>/", transfer.AmountDollarProcess, name="amount-dollar-process" ),
    path("transfer-dollar-confirm/<dollar_number>/<transaction_id>", transfer.TransferDollarConfirm, name="transfer-dollar-confirm" ),
    path("transfer-dollar-process/<dollar_number>/<transaction_id>", transfer.TransferDollarProcess, name="transfer-dollar-process" ),
    path("transfer-dollar-completed/<dollar_number>/<transaction_id>", transfer.TransferDollarCompleted, name="transfer-dollar-completed" ),
    
    
    path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name="amount-transfer-process" ),
    path("transfer-confirmation/<account_number>/<transaction_id>", transfer.TransferConfirmation, name="transfer-confirmation" ),
    path("transfer-process/<account_number>/<transaction_id>", transfer.TransferProcess, name="transfer-process" ),
    path("transfer-completed/<account_number>/<transaction_id>", transfer.TransferCompleted, name="transfer-completed" ),

    #transactions

    path("transactions/", transaction.transaction_list, name="transactions"),
    path("transaction_detail/<transaction_id>", transaction.transaction_detail, name="transaction_detail"),

    #payment Request
    path("request-search-account/", payment_request.SearchUsersRequest, name="request-search-account"),
    path("amount-request/<account_number>", payment_request.AmountRequest, name="amount-request"),
    path("amount-request-process/<account_number>/", payment_request.AmountRequestProcess, name="amount-request-process"),
    path("amount-request-confirmation/<account_number>/<transaction_id>/", payment_request.AmountRequestConfirmation, name="amount-request-confirmation"),
    path("amount-request-final-process/<account_number>/<transaction_id>/", payment_request.AmountRequestFinalProcess, name="amount-request-final-process"),
    path("amount-request-completed/<account_number>/<transaction_id>/", payment_request.RequestCompleted, name="amount-request-completed"),

    # Request Settlement
    path("settlement-confirmation/<account_number>/<transaction_id>/", payment_request.settlement_confirmation, name="settlement-confirmation"),
    path("settlement-processing/<account_number>/<transaction_id>/", payment_request.settlement_processing, name="settlement-processing"),
    path("delete-request/<account_number>/<transaction_id>/", payment_request.deletepaymentrequest, name="delete-request"),
    path("delete-reciever/<account_number>/<transaction_id>/", payment_request.deleterecieverequest, name="delete-reciever"),
    path("settlement-completed/<account_number>/<transaction_id>/", payment_request.SettlementCompleted, name="settlement-completed"),
    
    

    #card payment
 
    path('process-payment/', credit_card.process_payment, name='process_payment'),
    path('payment-failed/', credit_card.process_payment, name='payment-failed'),
    path("card/<card_id>/", credit_card.card_detail, name="card-detail"),
    path("delete_card/<card_id>/", credit_card.delete_card, name="delete_card"),
    path("fund-credit-card/<card_id>/", credit_card.fund_credit_card, name="fund-credit-card"),
    path("withdraw_fund/<card_id>/", credit_card.withdraw_fund, name="withdraw_fund"),

    #money-exchange
    path('aza-exchange/', money_exchange.money_exchange, name='money_exchange'),
    path("aza-exchange-process/", money_exchange.DollarTransferProcess, name="money_exchange_process" ),
    path("aza-exchange-confirmation/<dollar_number>/<transaction_id>/", money_exchange.exchangeconfirmation, name="exchange-confirmation"),
    path("aza-exchange-confirmrate/<dollar_number>/<account_number>/<transaction_id>/", money_exchange.exchangeconfirmrate, name="exchange-confirmrate"),
    path("aza-exchange-rate/<dollar_number>/<account_number>/<transaction_id>/", money_exchange.exchangerateprocess, name="exchange-rateprocess"),
    path("exchange-completed/<dollar_number>/<account_number>/<transaction_id>", money_exchange.ExchangeCompleted, name="exchange-completed" ),





]
