"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successfull(self):
        """Test creating a user with an email is successful. """
        email = 'test@abv.bg'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['kalin@ABV.bg', 'kalin@abv.bg'],
            ['kalin@Gmail.com', 'kalin@gmail.com'],
            ['KALIN@abv.BG', 'KALIN@abv.bg'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'parola123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating user without email is raising a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'parola123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser('kalin2@abv.bg', 'parola123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
