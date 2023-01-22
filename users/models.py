"""User models."""
from datetime import datetime

from django.db import models

get_cur_time = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")


def upload_to(instance, filename):
    """Set upload path and filename for uploaded images."""
    return 'images/{filename}'.format(filename=filename)


class HackUser(models.Model):
    """The main user model."""

    email = models.EmailField(max_length=100, default="")
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    registered = models.CharField(max_length=50, default=get_cur_time, blank=True)
    token = models.CharField(max_length=10000, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.username
