from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from drf_spectacular.utils import extend_schema_field

User = get_user_model()


class Post(models.Model):
    """Text."""

    content = models.TextField(max_length=2500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @extend_schema_field({"type": "integer"})
    def total_likes(self):
        ratings = Rating.objects.filter(post=self)
        return len(ratings)

    @extend_schema_field({"type": "string"})
    def liked_by(self):
        ratings = Rating.objects.filter(post=self)
        users = [rating.user for rating in ratings]
        return f"{users}"

    def __str__(self):
        return f"Author:{self.author} - {self.content[:50]} ..."


class Rating(models.Model):
    """Text."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = (("user", "post"),)
        index_together = (("user", "post"),)
