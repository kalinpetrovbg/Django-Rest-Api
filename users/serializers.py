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

    def validate(self, data):
        """
        Check if name starts with capital letter.
        :param data: request data
        :return: request data
        """
        name = data["name"]
        if name:
            start_letter = name[0]
            if start_letter.islower():
                raise serializers.ValidationError("Name must start with capital letter.")
        return data

    class Meta:
        model = get_user_model()
        fields = ("name", "description")
