"""Post views."""
import json
import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tweets.models import HackPost
from tweets.serializers import PostSerializer, PostValidator
from django.contrib.auth import get_user_model

from users.views import is_authorized

logger = logging.getLogger(__name__)
logging.basicConfig(filename="debug.log", level=logging.DEBUG)


AUTH_ERROR = {
    "Error_code": status.HTTP_401_UNAUTHORIZED,
    "Error_Message": "Authentication failed. Please login",
}


def get_user_object(user_id: int = None) -> object:
    """
    Returns User object corresponding to the user_id.
    :param user_id: int
    :return: get_user_model
    """
    return get_user_model().objects.get(id=user_id)


@api_view(["POST"])
def create_post(request):
    """
    Creating a new post.
    Input:
        user_id: (mandatory) <int> get_user_model id
        content: (mandatory) <str> Post's text
    Output: Post obbject of the newly created post.
    """
    if request.method == "POST":
        author_id = request.query_params.get("user_id")
        post_content = request.query_params.get("content")

        if is_authorized(request, author_id):
            validate = PostValidator(request.query_params, request.FILES)

            if validate.is_valid():
                error = {
                    "Error_code": status.HTTP_400_BAD_REQUEST,
                    "Error_Message": "Invalid user or missing content",
                }
                logger.error(error)
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

            try:
                user = get_user_object(author_id)
                new_post = HackPost(author=user, content=post_content)
                new_post.save()
                serializer = PostSerializer(new_post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                error = {
                    "Error_code": status.HTTP_400_BAD_REQUEST,
                    "Error_Message": "User Does not exist",
                }
                logger.error(e)
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(AUTH_ERROR, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["PUT"])
def like(request, post_id=None):
    """
    Like a specific post by a user.
    Input:
        user_id (mandatory) <int>
    Output: Post object which has been liked.
    """
    try:
        user_id = request.query_params.get("user_id")
        user = get_user_object(user_id)

        if is_authorized(request, user_id):
            post = HackPost.objects.get(id=post_id)
            liked_already = post.liked_by.filter(id=user_id).exists()
            if not liked_already:
                post.liked_by.add(user)
                post.likes += 1
                post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(AUTH_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Error liking the post!",
        }
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def dislike(request, post_id=None):
    """
    Dislike a specific post by a user.
    Input:
        user_id (mandatory) <int>
    Output: Post object which has been disliked.
    """
    try:
        user_id = request.query_params.get("user_id")
        user = get_user_object(user_id)

        if is_authorized(request, user_id):
            post = HackPost.objects.get(id=post_id)
            liked_already = post.liked_by.filter(id=user_id).exists()
            if liked_already:
                post.liked_by.remove(user)
                post.likes -= 1
                post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(AUTH_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Error disliking the post",
        }
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def remove_post(request, post_id: int = None):
    """
    Marks a post for deletion.
    :param request: request
    :param post_id: int
    Output: Post object that was marked for deletion.
    """
    try:
        post = HackPost.objects.get(id=post_id)
        user_id = post.author.id
        if is_authorized(request, user_id):
            serializer = PostSerializer(post)
            post.published = False
            post.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(AUTH_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "This post no longer exists",
        }
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def all_posts(request):
    """
    For debugging purpose only.
    :return : Postserializer objects
    """
    posts = HackPost.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def feed(request):
    """
    Return a list with last 20 posts that are not marked for deletion.
    :return : Postserializer objects
    """
    posts = HackPost.objects.filter(published=True).order_by("-id")
    serializer = PostSerializer(posts[:20], many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
