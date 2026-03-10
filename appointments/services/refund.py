from django.core.exceptions import ValidationError
from django.db import transaction

from appointments.models import ServiceRecord
from wallets.models import ClientWalletTransaction
from wallets.services.transactions import create_wallet_transaction


def refund(appointment: ServiceRecord):
    if appointment.status != ServiceRecord.Status.COMPLETED:
        raise ValidationError("Refund allowed only for completed service")

    if ClientWalletTransaction.objects.filter(
        service_record=appointment,
        type=ClientWalletTransaction.Type.REFUND,
    ).exists():
        raise ValidationError("Refund already processed")

    if appointment.service_price is None:
        raise ValidationError("Service price not recorded")

    appointment_price = appointment.service_price
    client_wallet = appointment.client.client_wallet

    with transaction.atomic():
        return create_wallet_transaction(
            wallet=client_wallet,
            amount=appointment_price,
            type=ClientWalletTransaction.Type.REFUND,
            service_record=appointment,
        )
