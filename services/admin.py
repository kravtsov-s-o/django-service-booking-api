from django.contrib import admin

from services.models import Service, SpecialistService


# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "base_price", "is_active")
    search_fields = ("title", "description")


@admin.register(SpecialistService)
class SpecialistServiceAdmin(admin.ModelAdmin):
    list_display = ("specialist", "service", "payout_type", "payout_value")
    list_filter = ("service", "payout_type")
    search_fields = (
        "specialist__user__username",
        "specialist__user__first_name",
        "specialist__user__last_name",
        "service__title",
        "service__description",
    )
