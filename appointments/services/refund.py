from django.core.exceptions import ValidationError
from django.db import transaction

from appointments.models import ServiceRecord
from wallets.models import ClientWalletTransaction
from wallets.services.transactions import create_wallet_transaction


def refund(appointment: ServiceRecord):
    """
    Refund the client for a completed service.

    Conditions:
    - Appointment must have COMPLETED status.
    - Refund can only be processed once.
    - Service price must be recorded.

    The refund creates a wallet transaction that returns
    the service amount to the client's wallet.
    """
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
            transaction_type=ClientWalletTransaction.Type.REFUND,
            service_record=appointment,
        )
