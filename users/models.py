from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Role(models.IntegerChoices):
        SPECIALIST = 1
        CLIENT = 2
        EMPLOYEE = 3

    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=Role.choices, default=Role.CLIENT, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self) -> str:
        if not self.first_name or not self.last_name:
            return f"{self.username}"
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class SpecialistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='specialist_profile')
    is_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Specialist'
        verbose_name_plural = 'Specialists'


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
