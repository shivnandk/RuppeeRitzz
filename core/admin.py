from django.contrib import admin
from core.models import Transactions , CreditCard

class TransactionsAdmin(admin.ModelAdmin):
    list_editable=['amount','status','transaction_type','receiver','sender']
    list_display=['user','amount','status','transaction_type','receiver','sender']

admin.site.register(Transactions,TransactionsAdmin)

class CreditCardAdmin(admin.ModelAdmin):
    list_editable=['amount','card_type']
    list_display=['user','amount','card_type']

admin.site.register(CreditCard,CreditCardAdmin)

