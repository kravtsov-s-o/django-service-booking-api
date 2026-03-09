from services.models import SpecialistService


def calculate_specialist_payout(service_price, specialist_service):
    if specialist_service.payout_type == SpecialistService.Type.FULL:
        return service_price

    return specialist_service.payout_value