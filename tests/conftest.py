from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from appointments.models import ServiceRecord
from services.models import Service, SpecialistService
from wallets.models import ClientWalletTransaction

User = get_user_model()


# ============================================================
# USERS
# ============================================================
@pytest.fixture
def user_factory(db):
    """
    Factory for creating user with different roles.
    """

    User = get_user_model()

    def create_user(**kwargs):
        defaults = {
            "email": "client@test.com",
            "username": "client",
            "password": "testpass123",
            "role": User.Role.CLIENT,
        }
        defaults.update(kwargs)

        return User.objects.create(**defaults)

    return create_user


@pytest.fixture
def superuser(db):
    """
    Create superuser
    """
    return User.objects.create_superuser(
        email="admin@test.com",
        username="admin",
        password="adminpass123",
    )


@pytest.fixture
def client_user(user_factory):
    """
    Minimal client user.
    Profile + wallet should be created via signals.
    """
    return user_factory(
        role=User.Role.CLIENT, email="client@test.loc", username="client"
    )


@pytest.fixture
def client_profile(client_user):
    """
    Returns client profile created via signals.
    """
    return client_user.client_profile


@pytest.fixture
def client_wallet(client_profile):
    """
    Returns client wallet created via signal.
    """
    return client_profile.client_wallet


@pytest.fixture
def specialist_user(user_factory):
    """
    Minimal specialist user.
    Profile should be created via signals.
    """
    return user_factory(
        role=User.Role.SPECIALIST, email="specialist@test.loc", username="specialist"
    )


@pytest.fixture
def specialist_profile(specialist_user):
    """
    Returns specialist profile created via signals.
    """
    return specialist_user.specialist_profile


@pytest.fixture
def owner_specialist_user(specialist_user):
    """
    Specialist as Admin user.
    """
    specialist_user.specialist_profile.is_owner = True
    specialist_user.specialist_profile.save(update_fields=["is_owner"])
    return specialist_user


@pytest.fixture
def employee_user(user_factory):
    """
    Minimal employee user.
    """
    return user_factory(role=User.Role.EMPLOYEE)


# ============================================================
# SERVICES
# ============================================================
@pytest.fixture
def create_service(db):
    """
    Create base service
    """
    return Service.objects.create(
        title="Lorem Ipsum",
        description="Lorem Ipsum",
        base_price=50,
        is_active=True,
    )


@pytest.fixture
def specialist_service_factory(db, specialist_profile, create_service):
    """
    Factory for specialist service.
    """

    def create_specialist_service(**kwargs):
        defaults = {
            "specialist": specialist_profile,
            "service": create_service,
            "payout_type": SpecialistService.Type.FULL,
            "payout_value": None,
            "is_active": True,
        }

        defaults.update(kwargs)

        return SpecialistService.objects.create(**defaults)

    return create_specialist_service


@pytest.fixture
def create_specialist_service(specialist_service_factory):
    """
    Connect Specialist Service with full price
    """
    return specialist_service_factory(payout_type=SpecialistService.Type.FULL)


@pytest.fixture
def create_specialist_service_fixed_price(specialist_service_factory):
    """
    Connect Specialist Service with fixed price
    """
    return specialist_service_factory(
        payout_type=SpecialistService.Type.FIXED, payout_value=100
    )


# ============================================================
# SERVICE RECORD - APPOINTMENTS
# ============================================================
@pytest.fixture
def service_record_factory(db, client_profile, specialist_profile, create_service):
    def create_service_record(**kwargs):
        defaults = {
            "client": client_profile,
            "specialist": specialist_profile,
            "service": create_service,
            "status": ServiceRecord.Status.PLANNED,
            "scheduled_at": timezone.now() - timedelta(hours=1),
        }
        defaults.update(kwargs)

        return ServiceRecord.objects.create(**defaults)

    return create_service_record


@pytest.fixture
def create_service_record(service_record_factory, create_specialist_service):
    """
    Create ServiceRecord.
    """
    return service_record_factory()


# ============================================================
# WALLETS - TRANSACTIONS
# ============================================================
@pytest.fixture
def transaction_factory(db):
    """
    Factory for creating transaction with different options.
    """

    def create_transaction(**kwargs):
        defaults = {
            "wallet": None,
            "amount": 100,
            "type": ClientWalletTransaction.Type.MANUAL_TOPUP,
            "balance_after": 0,
            "service_record": None,
        }
        defaults.update(kwargs)

        return ClientWalletTransaction.objects.create(**defaults)

    return create_transaction


@pytest.fixture
def transaction_manual_topup(transaction_factory, client_wallet):
    """
    Create manual topup transaction.
    """
    return transaction_factory(wallet=client_wallet, amount=100)


@pytest.fixture
def transaction_service_charge(
    transaction_factory, client_wallet, create_service_record
):
    """
    Create Service Charge transaction.
    """
    return transaction_factory(
        wallet=client_wallet,
        amount=100,
        type=ClientWalletTransaction.Type.SERVICE_CHARGE,
        service_record=create_service_record,
    )


@pytest.fixture
def transaction_service_refund(
    transaction_factory, client_wallet, create_service_record
):
    """
    Create Service Refund transaction.
    """
    return transaction_factory(
        wallet=client_wallet,
        amount=100,
        type=ClientWalletTransaction.Type.REFUND,
        service_record=create_service_record,
    )
