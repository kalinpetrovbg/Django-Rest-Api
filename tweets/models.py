"""Post models."""

from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model


class HackPost(models.Model):
    """Model for the post objects."""

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, null=True)
    liked_by = models.ManyToManyField(get_user_model(), related_name="liked_users", blank=True)
    likes = models.IntegerField(default=0)
    published = models.BooleanField(default=True)
    posted_on = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name = 'Post'
