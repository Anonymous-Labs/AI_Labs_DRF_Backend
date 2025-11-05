from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def validate_email(self, value):
        """Check if email is already registered and verified"""
        if User.objects.filter(email=value, is_verified=True).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """Check if username is already taken"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')

        try:
            otp = OTP.objects.filter(email=email, is_used=False).latest('created_at')
            if not otp.is_valid():
                raise serializers.ValidationError({"otp_code": "OTP has expired. Please request a new one."})
            if otp.otp_code != otp_code:
                raise serializers.ValidationError({"otp_code": "Invalid OTP code."})
            attrs['otp'] = otp
        except OTP.DoesNotExist:
            raise serializers.ValidationError({"otp_code": "No OTP found for this email. Please request a new one."})

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'is_verified', 'date_joined']

