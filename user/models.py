from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import string


class User(AbstractUser):
    MANUAL = "MANUAL"
    GOOGLE = "GOOGLE"
    ACCOUNT_TYPE_CHOICES = [(MANUAL, "Manual"), (GOOGLE, "Google")]

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default=MANUAL)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class OTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP for {self.email} - {self.otp_code}"

    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))

    def is_valid(self):
        """Check if OTP is valid (not used and not expired)"""
        return not self.is_used and timezone.now() < self.expires_at
