import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model representing a user on the platform.

    Note that authentication/registration for users is done through keycloak."""
    org = models.ForeignKey(to="organisations.Organisation", on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    @property
    def initials(self):
        return "".join([c[0] for c in
                        self.get_full_name().split(" ")]) if self.get_full_name() else ""


def generate_device_api_key():
    """Generates a unique 64 chars API key"""
    key = secrets.token_urlsafe(48)  # 48 bytes = 64 chars
    if Device.objects.filter(api_key=key).exists():
        return generate_device_api_key()
    return key


class Device(models.Model):
    """Model holding all the info on a device. A device is something a user can use
    to record new recordings. Typically, that's going to be the desktop app."""
    created_at = models.DateTimeField(auto_now_add=True)
    is_key_exchanged = models.BooleanField(default=False)
    token = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    application = models.CharField(max_length=64)
    release = models.CharField(max_length=64)
    api_key = models.CharField(max_length=64, unique=True,
                               default=generate_device_api_key)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
