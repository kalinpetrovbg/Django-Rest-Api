"""User models."""
from django.utils import timezone

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


from users.managers import CustomUserManager


def upload_to(instance, filename):
    """Set upload path and filename for uploaded images."""
    return 'images/{filename}'.format(filename=filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Defining a custom user based on email address."""

    email = models.EmailField(_('email address'), unique=True)

    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=10000, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ("-id",)
        verbose_name = 'User'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
