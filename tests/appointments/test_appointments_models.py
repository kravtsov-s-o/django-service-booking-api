from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from appointments.models import ServiceRecord


def test_create_service_record(create_service_record):
    assert create_service_record is not None
    assert create_service_record.status == ServiceRecord.Status.PLANNED


def test_can_transition_planned_completed(create_service_record):
    assert create_service_record.can_transition(ServiceRecord.Status.COMPLETED)


def test_can_transition_planned_canceled(create_service_record):
    assert create_service_record.can_transition(ServiceRecord.Status.CANCELLED)


def test_can_transition_completed_canceled(service_record_factory):
    record = service_record_factory(status=ServiceRecord.Status.COMPLETED)

    with pytest.raises(ValidationError):
        record.can_transition(new_status=ServiceRecord.Status.CANCELLED)


def test_can_transition_completed_planned(service_record_factory):
    record = service_record_factory(status=ServiceRecord.Status.COMPLETED)

    with pytest.raises(ValidationError):
        record.can_transition(new_status=ServiceRecord.Status.PLANNED)


def test_can_transition_cancelled_completed(service_record_factory):
    record = service_record_factory(status=ServiceRecord.Status.CANCELLED)

    with pytest.raises(ValidationError):
        record.can_transition(new_status=ServiceRecord.Status.COMPLETED)


def test_can_transition_cancelled_planned(service_record_factory):
    record = service_record_factory(status=ServiceRecord.Status.CANCELLED)

    with pytest.raises(ValidationError):
        record.can_transition(new_status=ServiceRecord.Status.PLANNED)


def test_can_transition_planned_completed_with_future_date(service_record_factory):
    record = service_record_factory(scheduled_at=timezone.now() + timedelta(days=1))

    with pytest.raises(ValidationError):
        record.can_transition(new_status=ServiceRecord.Status.COMPLETED)
