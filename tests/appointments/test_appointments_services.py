import pytest
from django.core.exceptions import ValidationError

from appointments.models import ServiceRecord
from appointments.services.completion import complete_service_record
from appointments.services.refund import refund
from wallets.models import ClientWalletTransaction


def test_service_record_completed(create_service_record):
    service_record = create_service_record
    complete_service_record(service_record)

    service_record.refresh_from_db()
    assert service_record.status == ServiceRecord.Status.COMPLETED
    assert service_record.service_price is not None
    assert service_record.specialist_payout is not None
    assert service_record.completed_at is not None

    transaction = ClientWalletTransaction.objects.get(
        service_record=service_record,
        type=ClientWalletTransaction.Type.SERVICE_CHARGE,
    )
    assert transaction.amount == -service_record.service_price


def test_service_record_refund(create_service_record):
    service_record = create_service_record
    complete_service_record(service_record)
    refund(service_record)

    transaction = ClientWalletTransaction.objects.get(
        service_record=service_record,
        type=ClientWalletTransaction.Type.REFUND,
    )
    assert transaction.amount == service_record.service_price


def test_refund_twice_raises_validation_error(create_service_record):
    service_record = create_service_record
    complete_service_record(service_record)
    refund(service_record)

    with pytest.raises(ValidationError):
        refund(service_record)


def test_refund_not_allowed_with_service_record_not_completed(create_service_record):
    service_record = create_service_record
    with pytest.raises(ValidationError):
        refund(service_record)


def test_refund_not_allowed_with_service_record_without_price(service_record_factory):
    service_record = service_record_factory(status=ServiceRecord.Status.COMPLETED)
    with pytest.raises(ValidationError):
        refund(service_record)
