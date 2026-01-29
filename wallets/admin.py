from django.contrib import admin

from wallets.models import ClientWallet, ClientWalletTransaction


# Register your models here.
@admin.register(ClientWallet)
class ClientWalletAdmin(admin.ModelAdmin):
    list_display = ("client", "balance", "created_at", "updated_at")
    list_filter = ("client",)


@admin.register(ClientWalletTransaction)
class ClientWalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "amount", "type", "service_record", "created_at")
    list_filter = ("type",)
