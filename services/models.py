from django.db import models


# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class SpecialistService(models.Model):
    class Type(models.IntegerChoices):
        FULL = 1
        FIXED = 2

    specialist = models.ForeignKey('users.SpecialistProfile', on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='specialists')
    payout_type = models.IntegerField(choices=Type.choices, default=Type.FIXED, db_index=True)
    payout_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.specialist} — {self.service}'

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['specialist', 'service'],
                name='unique_specialist_service'
            )
        ]
