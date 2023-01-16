from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Text."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    http_method_names = ["get", "post", "delete"]

    @action(detail=True, methods=["POST"])
    def rate_post(self, request, pk=None):
        """Text."""
        if "like" in request.data:

            post = Post.objects.get(id=pk)
            user = request.user

            response = {"message": f'{user} like this post "{post.content}"'}

            try:
                rating = Rating.objects.get(user=user.id, post=post.id)
                rating.likes += 1
                rating.save()
            except Exception:
                Rating.objects.create(user=user, post=post, likes=1)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {"message": "something went wrong"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    """Text."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    http_method_names = ["get", "post"]
