from django.contrib import admin

from appointments.models import ServiceRecord


# Register your models here.
@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'specialist',
        'service',
        'scheduled_at',
        'status',
        'completed_at',
    )
    list_filter = ('specialist', 'service', 'status', 'completed_at')
    search_fields = (
        'client__user__username',
        'client__user__first_name',
        'client__user__last_name',
        'specialist__user__username',
        'specialist__user__first_name',
        'specialist__user__last_name',
        'service__title',
    )