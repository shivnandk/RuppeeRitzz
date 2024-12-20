from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from core.models import Transactions
from decimal import Decimal

@login_required
def SearchUserRequest(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        account=account.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct()

    context={
        "account":account,
        "query":query,
    }    

    return render(request, "payment_request/search-users.html",context)

@login_required
def AmountRequest(request, account_number):
    account=Account.objects.get(account_number=account_number)
    context={
        "account":account,
    }    

    return render(request, "payment_request/amount-request.html",context)


@login_required
def AmountRequestProcess(request, account_number):
    account = Account.objects.get(account_number=account_number)

    sender = request.user
    receiver = account.user

    sender_account = request.user.account
    receiver_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")
        
        new_request = Transactions.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            sender=sender,
            receiver=receiver,
            sender_account=sender_account,
            receiver_account=receiver_account,
            status="request_processing",
            transaction_type="request",
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "Error Occurred. Try Again Later.")
        return redirect("account:dashboard")

@login_required
def AmountRequestConfirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transactions.objects.get(transaction_id=transaction_id)

    context = {
        "account":account,
        "transaction":transaction,
    }
    return render(request, "payment_request/amount-request-confirmation.html", context)

@login_required
def AmountRequestFinalProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transactions.objects.get(transaction_id=transaction_id)

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            transaction.status = "request_sent"
            transaction.save()

            messages.success(request, "Your payment request have been sent successfully.")
            return redirect("core:amount-request-completed" ,account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "An error occured try again later")
            return redirect("account:dashboard")


@login_required
def RequestCompleted(request, account_number , transaction_id):
    transaction = Transactions.objects.get(transaction_id=transaction_id)
    account = Account.objects.get(account_number=account_number)
    context = {
        "account":account,
        "transaction":transaction,
    }
    return render(request, "payment_request/amount-request-completed.html", context)

######################### Settled #######################

@login_required
def settlement_confirmation(request,account_number, transaction_id):
    transaction = Transactions.objects.get(transaction_id=transaction_id)
    account = Account.objects.get(account_number=account_number)
    context = {
        "account":account,
        "transaction":transaction,
    }
    return render(request, "payment_request/settlement-confirmation.html", context)

@login_required
def settlement_processing(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transactions.objects.get(transaction_id=transaction_id)

    sender = request.user 
    sender_account = request.user.account ## me, 

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request, "Insufficient Funds, fund your account and try again.")
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.status = "request_settled"
                transaction.save()

                messages.success(request, f"Settled to {account.user.kyc.full_name} was successfull.")
                return redirect("core:settlement-completed", account.account_number, transaction.transaction_id)

        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("core:settlement-confirmation", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "Error Occured")
        return redirect("account:settlement-completed" , account.account_number, transaction.transaction_id)

@login_required
def SettlementCompleted(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transactions.objects.get(transaction_id=transaction_id)
    
    context = {
            "account":account,
            "transaction":transaction,
        }
    return render(request, "payment_request/settlement-completed.html", context)

@login_required
def DeletePaymentRequest(request, account_number ,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transactions.objects.get(transaction_id=transaction_id)

    if request.user == transaction.user:
        transaction.delete()
        messages.success(request, "Payment Request Deleted Sucessfully")
        return redirect("core:transaction")
    
    


