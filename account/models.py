from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL  


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not username:
            raise ValueError("Username must be provided")
        if not phone_number:
            raise ValueError("Phone number must be provided")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)

        # normal user = inactive
        if extra_fields.get("is_superuser") is not True:
            user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, email, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name  = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    # Tracking fields
    last_login_device = models.CharField(max_length=255, blank=True, null=True)
    last_ip = models.GenericIPAddressField(blank=True, null=True)
    last_logout = models.DateTimeField(blank=True, null=True)
    login_count = models.PositiveIntegerField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    def __str__(self):
        return self.email




# Login Ip History --------------------------------------------------
class LoginIPHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ip_history")
    ip_address = models.CharField(max_length=45)  # ipv6 ok
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.user} @ {self.ip_address} on {self.timestamp}"


# Login Device ----------------------------------------------------------
class LoginDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    device_name = models.CharField(max_length=255, default="Unknown Device")
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    last_used = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    refresh_token = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("-last_used",)

    def __str__(self):
        return f"{self.user} - {self.device_name} ({self.ip_address})"
