"""
Tests for the user API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


REGISTER_USER_URL = reverse("user:register")
TOKEN_URL = reverse("user:token")
PROFILE_URL = reverse("user:profile")


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
            "email": "kalin11@abv.bg",
            "password": "kalin123",
            "name": "Kalin Petrov",
        }

        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_if_email_already_exists(self):
        """Test if there is already an user with the same email."""
        payload = {
            "email": "kalin11@abv.bg",
            "password": "kalin123",
            "name": "Kalin Petrov",
        }

        create_user(**payload)
        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_too_short(self):
        """Test if password is less thant 5 characters."""
        payload = {
            "email": "kalin6@abv.bg",
            "password": "ka",
            "name": "Kalin Petrov",
        }

        res = self.client.post(REGISTER_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        users_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(users_exists)

    def test_create_token_for_user(self):
        """Test generating token for valid credetials."""
        user_details = {
            "name": "Kalin Petrov",
            "email": "kalin@gmail.com",
            "password": "pass134",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_with_bad_credentials(self):
        """Test returns error if credentials are invalid."""
        create_user(email="kalin2@gmail.com", password="pass12345")

        payload = {"email": "kalin2@gmail.com", "password": "wrong12345"}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_black_password(self):
        """Test using blank password returns an error."""
        payload = {"email": "kalin3@gmail.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test the private features of the user API."""

    def setUp(self):
        self.user = create_user(
            email="kalin55@abv.bg",
            password="pass12345",
            name="Kalin Petrov",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {"name": "Peter Petrov", "password": "newpassword1234"}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
