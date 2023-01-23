"""Serializers for the user API view."""
from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""

    class Meta:
        model = get_user_model()
        fields = ("name", "description")
