from django.urls import path

from . import views

urlpatterns = [
    path("create", views.create),
    path("login", views.login),
    path("logout/<int:user_id>", views.logout),
    path("update/<int:user_id>", views.update_account),
    path("total_likes/<int:user_id>", views.total_likes),
    path("total_posts/<int:user_id>", views.total_posts),
    path("feed/<int:user_id>", views.feed),
    path("users", views.users),  # debugging
]
