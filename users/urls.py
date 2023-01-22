from django.urls import path

from . import views

urlpatterns = [
    path("create", views.create),
    path("login", views.login),
    path("logout/<int:user_id>", views.logout),
    path("update/<int:user_id>", views.update_account),
    path("total_likes/<int:user_id>", views.total_likes),
    path("timeline/<int:user_id>", views.timeline),
    path("token", views.get_token),
    path("auth", views.authentication),
    path("users", views.users),  # debugging
]
