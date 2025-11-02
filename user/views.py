from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db import transaction
from datetime import timedelta
from django.template.loader import render_to_string
from django.conf import settings
import os
from utils.email import send_email_with_backend
from .serializers import SignupSerializer, OTPVerificationSerializer, UserSerializer
from .models import OTP

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    User signup endpoint that creates a user account and sends OTP via email.
    """
    serializer = SignupSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        first_name = serializer.validated_data.get('first_name', '')
        last_name = serializer.validated_data.get('last_name', '')

        # Check if user already exists but is not verified
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'is_active': False,  # User is inactive until verified
                'is_verified': False,
            }
        )

        if not created:
            # If user exists, update the details
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        # Set password
        user.set_password(password)
        user.save()

        # Invalidate any existing unused OTPs for this email
        OTP.objects.filter(email=email, is_used=False).update(is_used=True)

        # Generate OTP
        otp_code = OTP.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)  # OTP valid for 10 minutes

        # Create OTP record
        OTP.objects.create(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at
        )

        # Send OTP email
        subject = 'Verify Your Email - AI Labs'
        html_message = render_to_string('user/otp_email.html', {
            'otp_code': otp_code,
            'username': username or email,
        })
        plain_message = f'Your OTP verification code is: {otp_code}. This code will expire in 10 minutes.'

        try:
            send_email_with_backend(
                subject=subject,
                message=plain_message,
                recipient_list=[email],
                html_message=html_message,
                backend_key="noreply",
                fail_silently=False,
            )
            return Response({
                'message': 'OTP has been sent to your email. Please verify to complete signup.',
                'email': email
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': 'Failed to send email. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    OTP verification endpoint that verifies the OTP and completes user signup/onboarding.
    """
    serializer = OTPVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        # Get the user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found. Please sign up again.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Mark OTP as used
        otp.is_used = True
        otp.save()

        # Activate and verify user
        user.is_active = True
        user.is_verified = True
        user.save()

        # Return user data
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Email verified successfully. Your account has been activated.',
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    """
    Resend OTP endpoint for users who didn't receive the OTP or it expired.
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Check if user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'error': 'User not found. Please sign up first.'
        }, status=status.HTTP_404_NOT_FOUND)

    # Check if user is already verified
    if user.is_verified:
        return Response({
            'message': 'Your email is already verified.'
        }, status=status.HTTP_200_OK)

    # Invalidate any existing unused OTPs for this email
    OTP.objects.filter(email=email, is_used=False).update(is_used=True)

    # Generate new OTP
    otp_code = OTP.generate_otp()
    expires_at = timezone.now() + timedelta(minutes=10)

    # Create new OTP record
    OTP.objects.create(
        email=email,
        otp_code=otp_code,
        expires_at=expires_at
    )

    # Send OTP email
    subject = 'Verify Your Email - AI Labs (Resend)'
    html_message = render_to_string('user/otp_email.html', {
        'otp_code': otp_code,
        'username': user.username or email,
    })
    plain_message = f'Your OTP verification code is: {otp_code}. This code will expire in 10 minutes.'

    try:
        send_email_with_backend(
            subject=subject,
            message=plain_message,
            recipient_list=[email],
            html_message=html_message,
            backend_key="noreply",
            fail_silently=False,
        )
        return Response({
            'message': 'OTP has been resent to your email.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Failed to send email. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Check if user exists and is verified before authentication
        username = request.data.get("username")
        if username:
            try:
                user = User.objects.get(username=username)
                if not user.is_verified:
                    return Response(
                        {
                            "error": "Please verify your email address before signing in. Check your email for the verification code."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
                if not user.is_active:
                    return Response(
                        {
                            "error": "Your account is inactive. Please contact support."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
            except User.DoesNotExist:
                pass  # Let the default authentication handle invalid credentials

        response = super().post(request, *args, **kwargs)
        
        # Get user from the validated credentials
        user = self.get_user(request.data["username"])
        user_serializer = UserSerializer(user)
        serialized_user = user_serializer.data

        return Response(
            {
                "refresh": response.data["refresh"],
                "access": response.data["access"],
                "user": serialized_user,
            },
            status=status.HTTP_200_OK
        )

    def get_user(self, username):
        return User.objects.get(username=username)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Decode the refresh token to get the user ID
        refresh_token = request.data.get("refresh")
        refresh = RefreshToken(refresh_token)
        user_id = refresh["user_id"]

        # Get the user
        user = User.objects.get(id=user_id)
        user_serializer = UserSerializer(user)
        serialized_user = user_serializer.data

        return Response(
            {
                "refresh": response.data["refresh"],
                "access": response.data["access"],
                "user": serialized_user,
            },
            status=status.HTTP_200_OK
        )


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def password_reset_link(request):
    """
    Send password reset link to user's email.
    """
    email = request.data.get("email")
    
    if not email:
        return Response(
            {"error": "Email is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Don't reveal if user exists for security reasons
        return Response(
            {"message": "If an account with this email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK,
        )

    # Check if user is verified
    if not user.is_verified:
        return Response(
            {"error": "Please verify your email address before resetting your password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Generate password reset token and user encoded ID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Construct the password reset link
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    reset_link = f"{frontend_url}/reset-password/{uid}/{token}/"

    # Send email with the reset link
    subject = "Password Reset Requested - AI Labs"
    plain_message = f"Click the link below to reset your password:\n{reset_link}\n\nThis link will expire in 24 hours."

    html_message = render_to_string('user/password_reset_email.html', {
        "frontend_url": frontend_url,
        "backend_url": os.getenv("BACKEND_URL", "http://localhost:8000"),
        "first_name": user.first_name or user.username,
        "reset_link": reset_link,
        "uid": uid,
        "token": token,
    })

    try:
        send_email_with_backend(
            subject=subject,
            message=plain_message,
            recipient_list=[email],
            html_message=html_message,
            backend_key="noreply",
            fail_silently=False,
        )
        return Response(
            {"message": "If an account with this email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": "Failed to send email. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def reset_password(request, uidb64, token):
    """
    Reset password using the token from the reset link.
    """
    new_password = request.data.get("new_password")
    
    if not new_password:
        return Response(
            {"error": "New password is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    # Validate password length
    if len(new_password) < 8:
        return Response(
            {"error": "Password must be at least 8 characters long."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response(
            {"error": "Invalid token or user ID."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if token is valid
    if not default_token_generator.check_token(user, token):
        return Response(
            {"error": "Invalid or expired token. Please request a new password reset link."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Set the new password for the user
    try:
        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"error": f"Failed to save new password: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
