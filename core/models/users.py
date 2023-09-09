from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid
from datetime import timedelta
from ..managers import UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import os
import jwt
from dotenv import load_dotenv
load_dotenv()
# Access the environment variables
secret_key = str(os.getenv("SECRET_KEY"))


class User(AbstractBaseUser, PermissionsMixin):
    # Hack to neglate this fields from the existing user model of Django
    username = models.CharField(blank=True, null=True, unique=True, max_length=255)
    password = models.CharField(blank=True, null=True, max_length=255)

    UID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_code = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # last_login and last_login (with this info we can send notifications to user who are login differently etc)
    last_login = models.DateTimeField(blank=True, null=True)
    last_logout_time = models.DateTimeField(blank=True, null=True)

    # date and time when this User was created
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "is_staff", "is_superuser"]

    objects = UserManager()

    def get_phone_number(self):
        return f"{self.country_code} {self.phone_number}"

    def user_token(self):
        token = AuthToken.objects.create(user=self)
        return token.key

    def generate_jwt_token(self):
        # JWT Token generation
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    def update_superuser_token(sender, user, request, **kwargs):
        if user.is_superuser:
            AuthToken.objects.filter(user=user).delete()
            AuthToken.objects.create(user=user)

    user_logged_in.connect(update_superuser_token)

    def check_superuser_token_validity(self, token: str) -> bool:
        token_expiry_time = timezone.now() - timedelta(hours=24)
        user_token_qs = AuthToken.objects.filter(
            user=self, created__gte=token_expiry_time, key=token
        )
        if not user_token_qs.exists():
            return False
        return True

    def get_last_login(self):
        return (
            self.last_login + timedelta(hours=5, minutes=30)
            if self.last_login
            else None
        )

    def get_display_name(self):
        try:
            return self.user_profile.get_display_name()
        except Exception:
            return ""

    def delete_expired_tokens(self) -> bool:
        token_expiry_time_in_days = timezone.now() - timedelta(
            days=settings.TOKEN_EXPIRY_TIME_IN_DAYS
        )
        AuthToken.objects.filter(
            user=self, created__lt=token_expiry_time_in_days
        ).delete()

    def check_user_token_validity(self, token: str) -> bool:
        token_expiry_time_in_days = timezone.now() - timedelta(
            days=settings.TOKEN_EXPIRY_TIME_IN_DAYS
        )
        user_token_qs = AuthToken.objects.filter(
            user=self, created__gte=token_expiry_time_in_days, key=token
        )
        if not user_token_qs.exists():
            return False

        self.delete_expired_tokens()
        token = user_token_qs.first()
        token.created = timezone.now()
        token.save()
        return True

    def perform_user_login(self):
        self.last_login = timezone.now()
        self.date_updated = timezone.now()
        self.save()

    def __str__(self):
        """Return a human readable representation of the User instance."""
        return f"Username: {self.username}, Name: {self.get_display_name()}"

    class Meta:
        app_label = "core"


class AuthToken(Token):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tokens",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "core"


class UserProfile(models.Model):
    user = models.OneToOneField(
        "User",
        blank=True,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="user_profile",
    )
    first_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    last_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    email = models.EmailField(max_length=255, blank=True, null=True, db_index=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "(first_name: {}, last_name: {}, email: {})".format(
            self.first_name, self.last_name, self.email
        )

    def has_active_profile(self) -> bool:
        return self.user.is_active

    def get_name_initials(self):
        if self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        else:
            return self.first_name[0].upper()

    def get_display_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name

    class Meta:
        app_label = "core"
