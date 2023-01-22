from rest_framework import serializers

from users.models import HackUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackUser
        fields = "__all__"
