from django.contrib import admin

from .models import PendingRegistration


@admin.register(PendingRegistration)
class PendingRegistrationAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "attempts", "created_at", "expires_at"]
    readonly_fields = ["password_hash", "otp_hash"]
