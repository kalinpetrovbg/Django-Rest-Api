from django.urls import path
from rest_framework import routers
from django.conf.urls import include

from posts.views import PostViewSet, RatingViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
