from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Post, Rating


class UserSerializer(serializers.ModelSerializer):
    """Text."""

    class Meta:
        """Text."""

        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        """Text."""
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class PostSerializer(serializers.ModelSerializer):
    """Text."""

    class Meta:
        """Text."""

        model = Post
        fields = ("id", "author", "content", "total_likes", "liked_by")


class RatingSerializer(serializers.ModelSerializer):
    """Text."""

    class Meta:
        """Text."""

        model = Rating
        fields = ("id", "likes", "post", "user")
