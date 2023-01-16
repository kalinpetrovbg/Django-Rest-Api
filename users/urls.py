"""
URL mappings for the user API.
"""
from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("delete/<int:pk>", views.DeleteUserView.as_view(), name="delete"),
]
