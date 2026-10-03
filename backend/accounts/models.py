
import random
from datetime import timedelta

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


OTP_VALID_MINUTES = 10
OTP_MAX_ATTEMPTS = 5


class PendingRegistration(models.Model):
    """Temporary signup record until the email OTP is verified."""

    username = models.CharField(max_length=150)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    otp_hash = models.CharField(max_length=255)
    attempts = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def is_expired(self):
        return timezone.now() > self.expires_at

    def has_attempts_left(self):
        return self.attempts < OTP_MAX_ATTEMPTS

    def check_otp(self, code):
        return check_password(str(code), self.otp_hash)

    def __str__(self):
        return f"Pending signup: {self.email}"

    @staticmethod
    def generate_code():
        return f"{random.randint(0, 999999):06d}"

    @classmethod
    def create_for(cls, username, email, raw_password):
        cls.objects.filter(email__iexact=email).delete()

        code = cls.generate_code()

        pending = cls.objects.create(
            username=username,
            email=email,
            password_hash=make_password(raw_password),
            otp_hash=make_password(code),
            expires_at=timezone.now()
            + timedelta(minutes=OTP_VALID_MINUTES),
        )

        return pending, code

    def refresh_code(self):
        code = self.generate_code()

        self.otp_hash = make_password(code)
        self.attempts = 0
        self.expires_at = (
            timezone.now()
            + timedelta(minutes=OTP_VALID_MINUTES)
        )

        self.save(
            update_fields=[
                "otp_hash",
                "attempts",
                "expires_at",
            ]
        )

        return code


class LoginOTP(models.Model):
    """Short-lived OTP used for passwordless login/recovery."""

    email = models.EmailField()
    otp_hash = models.CharField(max_length=255)
    attempts = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["email", "created_at"]
            )
        ]

    def is_expired(self):
        return timezone.now() > self.expires_at

    def has_attempts_left(self):
        return self.attempts < OTP_MAX_ATTEMPTS

    def check_otp(self, code):
        return check_password(
            str(code),
            self.otp_hash
        )

    @staticmethod
    def generate_code():
        return f"{random.randint(0, 999999):06d}"

    @classmethod
    def create_for(cls, email):
        cls.objects.filter(
            email__iexact=email
        ).delete()

        code = cls.generate_code()

        item = cls.objects.create(
            email=email,
            otp_hash=make_password(code),
            expires_at=(
                timezone.now()
                + timedelta(
                    minutes=OTP_VALID_MINUTES
                )
            ),
        )

        return item, code

    def refresh_code(self):
        code = self.generate_code()

        self.otp_hash = make_password(code)
        self.attempts = 0
        self.expires_at = (
            timezone.now()
            + timedelta(
                minutes=OTP_VALID_MINUTES
            )
        )

        self.save(
            update_fields=[
                "otp_hash",
                "attempts",
                "expires_at",
            ]
        )

        return code

    def __str__(self):
        return f"Login OTP: {self.email}"
