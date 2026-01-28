from django.db import models


# Create your models here.
class ServiceRecord(models.Model):
    class Status(models.IntegerChoices):
        PLANNED = 1
        COMPLETED = 2
        CANCELLED = 3

    client = models.ForeignKey('users.ClientProfile', on_delete=models.CASCADE, related_name='service_records')
    specialist = models.ForeignKey('users.SpecialistProfile', on_delete=models.CASCADE, related_name='service_records')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='service_records')
    scheduled_at = models.DateTimeField()
    status = models.IntegerField(choices=Status.choices, default=Status.PLANNED, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    specialist_payout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.specialist} - {self.service} - {self.scheduled_at}"

    class Meta:
        ordering = ['-scheduled_at']
        verbose_name = 'Service Record'
        verbose_name_plural = 'Service Records'
