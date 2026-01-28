from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import SpecialistProfile, ClientProfile

# Register your models here.
User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    model = User


@admin.register(SpecialistProfile)
class SpecialistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_owner', 'created_at')
    list_filter = ('is_owner',)
    search_fields = ('user__email', 'user__username')


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email', 'user__username')
