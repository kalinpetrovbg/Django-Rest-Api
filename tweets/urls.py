from django.urls import path

from . import views

urlpatterns = [
    path("create", views.create_post),
    path("like/<int:post_id>", views.like),
    path("dislike/<int:post_id>", views.dislike),
    path("delete/<int:post_id>", views.remove_post),
    path("feed", views.feed),
    # path("posts", views.all_posts) for debuggin purposes
]
