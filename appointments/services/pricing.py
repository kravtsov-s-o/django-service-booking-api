from decimal import Decimal

from services.models import SpecialistService


def calculate_specialist_payout(
    service_price: Decimal, specialist_service: SpecialistService
) -> Decimal:
    """
    Calculate the specialist payout for a service.

    Rules:
    - FULL  → specialist receives the full service price
    - FIXED → specialist receives a predefined payout value
    """
    if specialist_service.payout_type == SpecialistService.Type.FULL:
        return service_price

    return specialist_service.payout_value
