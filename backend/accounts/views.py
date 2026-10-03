
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    PendingRegistration,
    LoginOTP,
    OTP_MAX_ATTEMPTS,
)
from careerbridge.email_utils import send_otp_email


def _user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }


def _tokens_for(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def _find_user(identifier):
    identifier = (identifier or "").strip()

    if not identifier:
        return None

    user = User.objects.filter(
        username__iexact=identifier
    ).first()

    if user:
        return user

    return User.objects.filter(
        email__iexact=identifier
    ).first()


def _send_auth_code(user, purpose):
    """
    LoginOTP stores OTPs by email only.

    The model does not have a purpose field, so the latest OTP
    for the email is used for both login and password recovery.
    """

    otp, code = LoginOTP.create_for(user.email)

    send_otp_email(
        user.email,
        code,
        purpose=purpose,
    )

    return otp


def _get_latest_otp(email):
    return (
        LoginOTP.objects
        .filter(email__iexact=email)
        .order_by("-created_at")
        .first()
    )


# ============================================================
# SIGNUP
# ============================================================

class RequestSignupOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = (
            request.data.get("username") or ""
        ).strip()

        email = (
            request.data.get("email") or ""
        ).strip().lower()

        password = (
            request.data.get("password") or ""
        )

        if not username or not email or not password:
            return Response(
                {
                    "error": (
                        "Username, email and password "
                        "are required."
                    )
                },
                status=400,
            )

        if len(password) < 6:
            return Response(
                {
                    "error": (
                        "Password must be at least "
                        "6 characters."
                    )
                },
                status=400,
            )

        if User.objects.filter(
            username__iexact=username
        ).exists():
            return Response(
                {
                    "error": "Username already exists."
                },
                status=400,
            )

        if User.objects.filter(
            email__iexact=email
        ).exists():
            return Response(
                {
                    "error": (
                        "An account with this email "
                        "already exists."
                    )
                },
                status=400,
            )

        try:
            _, code = PendingRegistration.create_for(
                username,
                email,
                password,
            )

            send_otp_email(
                email,
                code,
                purpose="signup",
            )

        except Exception as exc:
            import traceback

            traceback.print_exc()

            return Response(
                {
                    "error": (
                        f"Email sending failed: {exc}"
                    )
                },
                status=503,
            )

        return Response(
            {
                "message": (
                    f"A verification code has been "
                    f"sent to {email}."
                ),
                "email": email,
            }
        )


class VerifySignupOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (
            request.data.get("email") or ""
        ).strip().lower()

        code = (
            request.data.get("code") or ""
        ).strip()

        if not email or not code:
            return Response(
                {
                    "error": (
                        "Email and code are required."
                    )
                },
                status=400,
            )

        try:
            pending = (
                PendingRegistration.objects
                .filter(email__iexact=email)
                .latest("created_at")
            )

        except PendingRegistration.DoesNotExist:
            return Response(
                {
                    "error": (
                        "No pending signup found "
                        "for this email."
                    )
                },
                status=404,
            )

        if pending.is_expired():
            pending.delete()

            return Response(
                {
                    "error": (
                        "This code has expired. "
                        "Please sign up again."
                    )
                },
                status=400,
            )

        if not pending.has_attempts_left():
            pending.delete()

            return Response(
                {
                    "error": (
                        "Too many incorrect attempts. "
                        "Please sign up again."
                    )
                },
                status=400,
            )

        if not pending.check_otp(code):
            pending.attempts += 1

            pending.save(
                update_fields=["attempts"]
            )

            remaining = max(
                0,
                OTP_MAX_ATTEMPTS - pending.attempts,
            )

            return Response(
                {
                    "error": (
                        "Incorrect verification code. "
                        f"{remaining} attempt(s) remaining."
                    )
                },
                status=400,
            )

        if (
            User.objects.filter(
                username__iexact=pending.username
            ).exists()
            or
            User.objects.filter(
                email__iexact=pending.email
            ).exists()
        ):
            pending.delete()

            return Response(
                {
                    "error": (
                        "This account was already "
                        "created. Please sign in."
                    )
                },
                status=400,
            )

        user = User(
            username=pending.username,
            email=pending.email,
        )

        user.password = pending.password_hash
        user.save()

        pending.delete()

        return Response(
            {
                "message": (
                    "Email verified and account "
                    "created successfully."
                ),
                "user": _user_payload(user),
                **_tokens_for(user),
            },
            status=201,
        )


class ResendSignupOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (
            request.data.get("email") or ""
        ).strip().lower()

        if not email:
            return Response(
                {
                    "error": "Email is required."
                },
                status=400,
            )

        try:
            pending = (
                PendingRegistration.objects
                .filter(email__iexact=email)
                .latest("created_at")
            )

        except PendingRegistration.DoesNotExist:
            return Response(
                {
                    "error": (
                        "No pending signup found "
                        "for this email."
                    )
                },
                status=404,
            )

        code = pending.refresh_code()

        try:
            send_otp_email(
                email,
                code,
                purpose="signup",
            )

        except Exception as exc:
            return Response(
                {
                    "error": (
                        "We could not send the new "
                        f"verification code: {exc}"
                    )
                },
                status=503,
            )

        return Response(
            {
                "message": (
                    "A new verification code "
                    "has been sent."
                )
            }
        )


# ============================================================
# PASSWORD LOGIN
# ============================================================

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = (
            request.data.get("username")
            or request.data.get("identifier")
            or request.data.get("email")
            or ""
        ).strip()

        password = (
            request.data.get("password") or ""
        )

        if not identifier or not password:
            return Response(
                {
                    "error": (
                        "Username/email and password "
                        "are required."
                    )
                },
                status=400,
            )

        user_record = _find_user(identifier)

        if user_record and not user_record.is_active:
            return Response(
                {
                    "error": (
                        "Account suspended. "
                        "Please contact administration."
                    )
                },
                status=403,
            )

        username_for_auth = (
            user_record.username
            if user_record
            else identifier
        )

        user = authenticate(
            username=username_for_auth,
            password=password,
        )

        if user is None:
            return Response(
                {
                    "error": (
                        "Invalid username/email "
                        "or password."
                    )
                },
                status=401,
            )

        if not user.is_active:
            return Response(
                {
                    "error": (
                        "Account suspended. "
                        "Please contact administration."
                    )
                },
                status=403,
            )

        return Response(
            {
                "message": "Login successful.",
                "user": _user_payload(user),
                **_tokens_for(user),
            }
        )


# ============================================================
# LOGIN OTP
# ============================================================

class RequestLoginOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = (
            request.data.get("identifier")
            or request.data.get("email")
            or ""
        ).strip()

        user = _find_user(identifier)

        if not user:
            return Response(
                {
                    "error": (
                        "No account was found for "
                        "that username or email."
                    )
                },
                status=404,
            )

        if not user.is_active:
            return Response(
                {
                    "error": (
                        "Account suspended. "
                        "Please contact administration."
                    )
                },
                status=403,
            )

        if not user.email:
            return Response(
                {
                    "error": (
                        "This account does not have "
                        "an email address for OTP login."
                    )
                },
                status=400,
            )

        try:
            _send_auth_code(
                user,
                "login",
            )

        except Exception as exc:
            return Response(
                {
                    "error": (
                        "Unable to send login OTP: "
                        f"{exc}"
                    )
                },
                status=503,
            )

        return Response(
            {
                "message": (
                    f"A login OTP has been sent "
                    f"to {user.email}."
                ),
                "email": user.email,
            }
        )


class VerifyLoginOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (
            request.data.get("email") or ""
        ).strip().lower()

        code = (
            request.data.get("code") or ""
        ).strip()

        if not email or not code:
            return Response(
                {
                    "error": (
                        "Email and code are required."
                    )
                },
                status=400,
            )

        otp = _get_latest_otp(email)

        if not otp:
            return Response(
                {
                    "error": (
                        "No active login OTP found. "
                        "Request a new code."
                    )
                },
                status=404,
            )

        if otp.is_expired():
            otp.delete()

            return Response(
                {
                    "error": (
                        "This OTP has expired. "
                        "Request a new one."
                    )
                },
                status=400,
            )

        if not otp.has_attempts_left():
            otp.delete()

            return Response(
                {
                    "error": (
                        "Too many incorrect attempts. "
                        "Request a new OTP."
                    )
                },
                status=400,
            )

        if not otp.check_otp(code):
            otp.attempts += 1

            otp.save(
                update_fields=["attempts"]
            )

            remaining = max(
                0,
                OTP_MAX_ATTEMPTS - otp.attempts,
            )

            return Response(
                {
                    "error": (
                        f"Incorrect OTP. "
                        f"{remaining} attempt(s) remaining."
                    )
                },
                status=400,
            )

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user:
            otp.delete()

            return Response(
                {
                    "error": (
                        "The account associated "
                        "with this OTP no longer exists."
                    )
                },
                status=404,
            )

        if not user.is_active:
            return Response(
                {
                    "error": (
                        "Account suspended. "
                        "Please contact administration."
                    )
                },
                status=403,
            )

        # LoginOTP has no used_at field, so delete the
        # successfully consumed OTP.
        otp.delete()

        return Response(
            {
                "message": "OTP login successful.",
                "user": _user_payload(user),
                **_tokens_for(user),
            }
        )


# ============================================================
# PASSWORD RESET
# ============================================================

class RequestPasswordResetOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (
            request.data.get("email") or ""
        ).strip().lower()

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user:
            return Response(
                {
                    "error": (
                        "No account was found "
                        "with that email."
                    )
                },
                status=404,
            )

        if not user.is_active:
            return Response(
                {
                    "error": (
                        "Account suspended. "
                        "Please contact administration."
                    )
                },
                status=403,
            )

        try:
            _send_auth_code(
                user,
                "reset",
            )

        except Exception as exc:
            return Response(
                {
                    "error": (
                        "Unable to send reset OTP: "
                        f"{exc}"
                    )
                },
                status=503,
            )

        return Response(
            {
                "message": (
                    "A password reset OTP has "
                    "been sent to your email."
                ),
                "email": email,
            }
        )


class ResetPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (
            request.data.get("email") or ""
        ).strip().lower()

        code = (
            request.data.get("code") or ""
        ).strip()

        new_password = (
            request.data.get("new_password") or ""
        )

        if len(new_password) < 6:
            return Response(
                {
                    "error": (
                        "New password must be at "
                        "least 6 characters."
                    )
                },
                status=400,
            )

        otp = _get_latest_otp(email)

        if not otp:
            return Response(
                {
                    "error": (
                        "No active password reset "
                        "OTP found."
                    )
                },
                status=404,
            )

        if otp.is_expired():
            otp.delete()

            return Response(
                {
                    "error": (
                        "This OTP has expired. "
                        "Request a new one."
                    )
                },
                status=400,
            )

        if not otp.has_attempts_left():
            otp.delete()

            return Response(
                {
                    "error": (
                        "Too many incorrect attempts. "
                        "Request a new OTP."
                    )
                },
                status=400,
            )

        if not otp.check_otp(code):
            otp.attempts += 1

            otp.save(
                update_fields=["attempts"]
            )

            remaining = max(
                0,
                OTP_MAX_ATTEMPTS - otp.attempts,
            )

            return Response(
                {
                    "error": (
                        f"Incorrect OTP. "
                        f"{remaining} attempt(s) remaining."
                    )
                },
                status=400,
            )

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user:
            otp.delete()

            return Response(
                {
                    "error": "User not found."
                },
                status=404,
            )

        user.set_password(new_password)

        user.save(
            update_fields=["password"]
        )

        otp.delete()

        return Response(
            {
                "message": (
                    "Password reset successfully. "
                    "You can now sign in with your "
                    "new password."
                )
            }
        )


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = (
            request.data.get("current_password")
            or ""
        )

        new_password = (
            request.data.get("new_password")
            or ""
        )

        confirm_password = (
            request.data.get("confirm_password")
            or ""
        )

        if not request.user.check_password(
            current_password
        ):
            return Response(
                {
                    "error": (
                        "Current password is incorrect."
                    )
                },
                status=400,
            )

        if len(new_password) < 6:
            return Response(
                {
                    "error": (
                        "New password must be at least "
                        "6 characters."
                    )
                },
                status=400,
            )

        if (
            confirm_password
            and new_password != confirm_password
        ):
            return Response(
                {
                    "error": (
                        "New password and confirmation "
                        "do not match."
                    )
                },
                status=400,
            )

        if request.user.check_password(
            new_password
        ):
            return Response(
                {
                    "error": (
                        "New password must be different "
                        "from your current password."
                    )
                },
                status=400,
            )

        request.user.set_password(
            new_password
        )

        request.user.save(
            update_fields=["password"]
        )

        return Response(
            {
                "message": (
                    "Password changed successfully. "
                    "Please sign in again with your "
                    "new password."
                )
            }
        )


# ============================================================
# ADMIN USERS
# ============================================================

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = (
            User.objects
            .all()
            .order_by("-date_joined")
        )

        data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "date_joined": user.date_joined,
                "resume_count": user.resumes.count(),
                "job_count": user.job_descriptions.count(),
                "match_count": user.match_results.count(),
                "interview_count": user.interview_sessions.count(),
            }
            for user in users
        ]

        return Response(
            {
                "count": len(data),
                "users": data,
            }
        )


class AdminToggleUserActiveView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            target = User.objects.get(
                id=user_id
            )

        except User.DoesNotExist:
            return Response(
                {
                    "error": "User not found."
                },
                status=404,
            )

        if target.id == request.user.id:
            return Response(
                {
                    "error": (
                        "You cannot suspend your "
                        "own admin account."
                    )
                },
                status=400,
            )

        if target.is_superuser:
            return Response(
                {
                    "error": (
                        "Superuser accounts cannot be "
                        "suspended from the student "
                        "admin panel."
                    )
                },
                status=400,
            )

        if (
            target.is_staff
            and not request.user.is_superuser
        ):
            return Response(
                {
                    "error": (
                        "Only a superuser can change "
                        "another staff account."
                    )
                },
                status=403,
            )

        target.is_active = not target.is_active

        target.save(
            update_fields=["is_active"]
        )

        return Response(
            {
                "message": (
                    "User account activated."
                    if target.is_active
                    else "User account suspended."
                ),
                "id": target.id,
                "is_active": target.is_active,
            }
        )

