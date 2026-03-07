from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import ClientProfile
from wallets.models import ClientWallet


@receiver(post_save, sender=ClientProfile)
def create_wallet_for_client(sender, instance, created, **kwargs):
    if created:
        ClientWallet.objects.create(client=instance)
