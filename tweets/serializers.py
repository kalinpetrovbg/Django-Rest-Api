from django import forms
from rest_framework import serializers

from tweets.models import HackPost


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackPost
        fields = "__all__"


class PostValidator(forms.Form):
    author = forms.CharField()
    content = forms.CharField()
