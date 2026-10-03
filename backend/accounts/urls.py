from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    RequestSignupOTPView,
    VerifySignupOTPView,
    ResendSignupOTPView,
    RequestLoginOTPView,
    VerifyLoginOTPView,
    RequestPasswordResetOTPView,
    ResetPasswordOTPView,
    ChangePasswordView,
    AdminUserListView,
    AdminToggleUserActiveView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("signup/request-otp/", RequestSignupOTPView.as_view(), name="signup-request-otp"),
    path("signup/verify-otp/", VerifySignupOTPView.as_view(), name="signup-verify-otp"),
    path("signup/resend-otp/", ResendSignupOTPView.as_view(), name="signup-resend-otp"),
    path("login/request-otp/", RequestLoginOTPView.as_view(), name="login-request-otp"),
    path("login/verify-otp/", VerifyLoginOTPView.as_view(), name="login-verify-otp"),
    path("password/request-otp/", RequestPasswordResetOTPView.as_view(), name="password-request-otp"),
    path("password/reset-otp/", ResetPasswordOTPView.as_view(), name="password-reset-otp"),
    path("password/change/", ChangePasswordView.as_view(), name="password-change"),
    path("admin/users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("admin/users/<int:user_id>/toggle-active/", AdminToggleUserActiveView.as_view(), name="admin-user-toggle-active"),
]
