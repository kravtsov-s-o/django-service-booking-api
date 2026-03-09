from django.core.exceptions import ValidationError
from django.utils import timezone

from appointments.models import ServiceRecord


def transition_impl(record: ServiceRecord, new_status: int):
    allowed = ServiceRecord.ALLOWED_TRANSITIONS[record.status]

    if new_status not in allowed:
        raise ValidationError("Invalid status transition")

    if (
        new_status == ServiceRecord.Status.COMPLETED
        and record.scheduled_at > timezone.now()
    ):
        raise ValidationError("Cannot complete appointment before scheduled time.")

    return True
