from django.db import transaction
from django.utils import timezone

from appointments.models import ServiceRecord
from appointments.services.pricing import calculate_specialist_payout
from services.models import SpecialistService
from wallets.models import ClientWalletTransaction
from wallets.services.transactions import create_wallet_transaction


def complete_service_record(appointment: ServiceRecord):
    """
    Complete a service appointment and charge the client's wallet.

    Workflow:
    1. Validate that the appointment can transition to COMPLETED.
    2. Calculate the service price and specialist payout.
    3. Charge the client wallet.
    4. Save financial snapshots on the appointment:
       - service_price
       - specialist_payout
       - completed_at

    All operations are executed inside a database transaction.
    """
    target_status = ServiceRecord.Status.COMPLETED

    if appointment.transition(target_status):
        with transaction.atomic():
            service_price = appointment.service.base_price

            specialist_service = SpecialistService.objects.get(
                service=appointment.service, specialist=appointment.specialist
            )

            specialist_payout = calculate_specialist_payout(
                service_price, specialist_service
            )

            create_wallet_transaction(
                wallet=appointment.client.client_wallet,
                amount=-service_price,
                transaction_type=ClientWalletTransaction.Type.SERVICE_CHARGE,
                service_record=appointment,
            )

            appointment.service_price = service_price
            appointment.specialist_payout = specialist_payout
            appointment.completed_at = timezone.now()
            appointment.status = target_status

            appointment.save(
                update_fields=[
                    "status",
                    "service_price",
                    "specialist_payout",
                    "completed_at",
                    "updated_at",
                ]
            )
