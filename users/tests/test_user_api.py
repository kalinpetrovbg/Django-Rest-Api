"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_is_successful(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'kalin5@abv.bg',
            'password': 'kalin123',
            'name': 'Kalin',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_if_email_already_exists(self):
        """Test if there is already an user with the same email."""
        payload = {
            'email': 'kalin6@abv.bg',
            'password': 'kalin123',
        }

        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_is_too_short(self):
        """Test if password is less thant 5 characters."""
        payload = {
            'email': 'kalin6@abv.bg',
            'password': 'ka',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        users_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(users_exists)