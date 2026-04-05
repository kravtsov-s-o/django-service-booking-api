import pytest
from django.db import IntegrityError

from services.models import SpecialistService


def test_create_service(create_service):
    assert create_service is not None


def test_specialist_service_unique_specialist_and_service(
    specialist_service_factory, specialist_profile, create_service
):
    specialist_service_factory(specialist=specialist_profile, service=create_service)

    with pytest.raises(IntegrityError):
        specialist_service_factory(
            specialist=specialist_profile, service=create_service
        )


def test_create_specialist_service_full_price(create_specialist_service):
    assert create_specialist_service is not None
    assert create_specialist_service.payout_type == SpecialistService.Type.FULL
    assert create_specialist_service.payout_value is None


def test_create_specialist_service_fixed_price(create_specialist_service_fixed_price):
    assert create_specialist_service_fixed_price is not None
    assert (
        create_specialist_service_fixed_price.payout_type
        == SpecialistService.Type.FIXED
    )
    assert create_specialist_service_fixed_price.payout_value is not None
