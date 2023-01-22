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
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=10000, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        ordering = ("-id",)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class HackUser(models.Model):
#     """The main user model."""
#
#     email = models.EmailField(max_length=100, default="")
#     username = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#     name = models.CharField(max_length=100, null=True, blank=True)
#     description = models.CharField(max_length=100, null=True, blank=True)
#     token = models.CharField(max_length=10000, null=True, blank=True)
#     photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
#
#     class Meta:
#         ordering = ("-id",)
#
#     def __str__(self):
#         return self.username
