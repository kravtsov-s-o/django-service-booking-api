from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import ClientProfile, SpecialistProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == User.Role.SPECIALIST:
        SpecialistProfile.objects.create(user=instance)

    elif instance.role == User.Role.CLIENT:
        ClientProfile.objects.create(user=instance)

    else:
        return
