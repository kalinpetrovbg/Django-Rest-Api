"""Post models."""
from datetime import datetime

from django.db import models

from users.models import HackUser

get_cur_time = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")


class HackPost(models.Model):
    """Model for the post objects."""

    author = models.ForeignKey(HackUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, null=True)
    timestamp = models.CharField(max_length=50, default=get_cur_time, blank=True)
    liked_by = models.ManyToManyField(HackUser, related_name="liked_users", blank=True)
    likes = models.IntegerField(default=0)
    published = models.BooleanField(default=True)
