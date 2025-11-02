from django.contrib import admin
from .models import User, OTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['is_verified', 'is_active', 'account_type']
    search_fields = ['email', 'username']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp_code', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['email', 'otp_code']
    readonly_fields = ['created_at', 'expires_at']
