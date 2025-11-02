from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('signin/', views.CustomTokenObtainPairView.as_view(), name='signin'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset-link/', views.password_reset_link, name='password_reset_link'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
]

