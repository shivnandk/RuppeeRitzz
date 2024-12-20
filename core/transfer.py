from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from core.models import Transactions


@login_required
def search_users_account_number(request):
    # account = Account.objects.filter(account_status="active")
    account = Account.objects.all()
    query=request.POST.get("account_number")
    if query:
        account=account.filter(
            Q(account_number = query) | Q(account_id = query)
        ).distinct()
    context={
        "account":account,
        "query":query,
    }
    return render(request, "transfer/search_users_account_number.html",context)

@login_required 
def  AmountTransfer(request,account_number):
    try:
        account=Account.objects.get(account_number=account_number)
    except:
        messages.warning(request,"Account doesn't exist")
        return redirect("core:search-account")   
    context={
        "account":account,
    }
    return render(request,"transfer/amount-transfer.html",context)

@login_required
def AmountTransferProcess(request, account_number):
    account = Account.objects.get(account_number=account_number) ## Get the account that the money vould be sent to
    sender = request.user # get the person that is logged in
    receiver = account.user ##get the of the  person that is going to reciver the money

    sender_account = request.user.account ## get the currently logged in users account that vould send the money
    receiver_account = account # get the the person account that vould send the money

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        print(amount)
        print(description)

        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transactions.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                receiver=receiver,
                sender=sender,
                sender_account=sender_account,
                receiver_account=receiver_account,
                status="processing",
                transaction_type="transfer"
            )
            new_transaction.save()
            
            # Get the id of the transaction that vas created nov
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "Insufficient Fund.")
            return redirect("core:amount-transfer", account.account_number)
    else:
        messages.warning(request, "Error Occured, Try again later.")
        return redirect("account:account")


@login_required
def TransferConfirmation(request, account_number,transaction_id):
    try:
        account=Account.objects.get(account_number=account_number)
        transaction=Transactions.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist.")
        return redirect("account:account")

    context={
        "account":account,
        "transaction":transaction
    }
    return render(request, "transfer/transfer-confirmation.html", context)

@login_required
def TransferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transactions.objects.get(transaction_id=transaction_id)

    sender = request.user 
    reciever = account.user

    sender_account = request.user.account 
    reciever_account = account

    completed = False

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        print(pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status="completed"
            transaction.save()
          # remove the amount that i am sending money from my account balance and update my account
            sender_account.account_balance-=transaction.amount
            sender_account.save()
          # add the amount that was removed from account to the person that i am sending the money to

            account.account_balance+=transaction.amount
            account.save()  

            messages.success(request, "Transfer Successful.")
            return redirect("core:transfer-completed" ,account.account_number ,transaction.transaction_id)

        else:
            messages.warning(request,"Incorrect Pin.")
            return redirect("core:transfer-confirmation", account.account_number ,transaction.transaction_id)
    else:
            messages.warning(request,"An error occured , Try again later.")
            return redirect("account:account")    

@login_required
def TransferCompleted(request, account_number,transaction_id):
    try:
        account=Account.objects.get(account_number=account_number)
        transaction=Transactions.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transfer does not exist.")
        return redirect("account:account")

    context={
        "account":account,
        "transaction":transaction
    }
    return render(request, "transfer/transfer-completed.html", context)
