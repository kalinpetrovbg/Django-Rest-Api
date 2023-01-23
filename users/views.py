"""User views."""
import datetime
import json
import logging

import jwt
from django.conf import settings
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tweets.models import HackPost
from tweets.serializers import PostSerializer
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
)

EXP_TIME = datetime.timedelta(hours=2)


def get_token(email):
    """
    Get Access token
    Input:
    email (mandatory) <str>
    password (mandatory) <str>
    Output: Token that expires in 120 minutes
    """
    try:
        user = get_user_model().objects.get(email=email)
        if user:
            try:
                payload = {
                    "id": user.id,
                    "email": user.email,
                    "exp": datetime.datetime.utcnow() + EXP_TIME,
                }
                token = {"token": jwt.encode(payload, key=settings.AUTH_TOKEN, algorithm='HS256')}
                return token

            except Exception as e:
                error = {
                    "Error_code": status.HTTP_400_BAD_REQUEST,
                    "Error_Message": "Error generating Auth Token",
                }
                logger.error(e)
                return Response(error, status=status.HTTP_403_FORBIDDEN)
        else:
            error = {
                "Error_code": status.HTTP_400_BAD_REQUEST,
                "Error_Message": "Invalid Email or Password",
            }
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Internal Server Error",
        }
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)



def authentication(request, user_id):
    """
    Login to the Application.
    Input:
        token (mandatory) <str> user's token
    Output: User object of the logged-in user.
    """
    try:
        token = request.session.get("authtoken").get("token")
        payload = jwt.decode(token, key=settings.AUTH_TOKEN, algorithms=['HS256'])
        user = get_user_model().objects.get(id=user_id)

        if payload.get("email") == user.email:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                "Error_code": status.HTTP_403_FORBIDDEN,
                "Error_Message": "Invalid User",
            }
            logger.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError) as e:
        error = {
            "Error_code": status.HTTP_403_FORBIDDEN,
            "Error_Message": "Token is Invalid/Expired",
        }
        logger.error(e)
        return Response(error, status=status.HTTP_403_FORBIDDEN)

    except Exception as e:
        error = {
            "Error_code": status.HTTP_403_FORBIDDEN,
            "Error_Message": "Internal Server Error",
        }
        logger.error(e)
        return Response(error, status=status.HTTP_403_FORBIDDEN)


def is_authorized(request, user_id):
    """
    Authorizing the user.
    :param request:
    :param user_id:
    :return:
    """
    validation = authentication(request, user_id)
    if validation.status_code == 200:
        return True
    else:
        return False


@api_view(["POST"])
def create(request):
    """
    Purpose: Create a new user
    Input:
    email (mandatory) <str> Chosen Username
    password (mandatory) <str> Chosen Password
    Output: User object of the created user
    """
    serializer = UserSerializer(data=request.query_params)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response("User was not created", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request, email=None, password=None):
    """
    Authenticate if username and password are correct.
    Input: email and password
    Output: return User object
    """
    email = request.query_params.get("email")
    password = request.query_params.get("password")
    try:
        user = get_user_model().objects.get(email=email)
        if user.password == password:
            token = get_token(email)
            user.token = token["token"]
            user.save()
            request.session["authtoken"] = token
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                "Error_code": status.HTTP_400_BAD_REQUEST,
                "Error_Message": "Invalid Email or Password",
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Invalid Username",
        }
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout(request, user_id=None):
    """Log out a specific user and delete his token.
    Input: user_id <int>
    Output: return the User object."""
    try:
        user = get_user_model().objects.get(id=user_id)
        user.token = ""
        user.save()
        request.session["authtoken"] = ""
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Invalid User ID",
        }
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_account(request, user_id):
    """
    Update Account Details.
    Input:
        user_id (mandatory) <int>
        name (optional) <str>
        description (optional) <str>
        photo (optional) <str>
    Output: User object of the updated user.
    """
    if is_authorized(request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)
            name = request.query_params.get("name")
            user.name = name
            description = request.query_params.get("description")
            user.description = description
            # photo = request.query_params.get("photo")
            # user.photo = photo
            user.save()

            serializer = UserSerializer(user)
            logger.error("Account Update successful")

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            error = {
                "Error_code": status.HTTP_400_BAD_REQUEST,
                "Error_Message": f"User with ID: {user_id} does not exist.",
            }
            logger.error("AccountUpdate: Error: " + str(e))
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    else:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Authentication failed. Please login",
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def total_likes(request, user_id):
    """
    Purpose: Returns total number of likes a user has.
    Input: user_id (mandatory) <int>
    :param request:
    :param user_id:
    :return: int
    """
    if is_authorized(request, user_id):
        posts = HackPost.objects.filter(author=user_id).aggregate(Sum("likes"))
        sum_likes = posts["likes__sum"]
        return Response(sum_likes)
    else:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Authentication failed. Please login",
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def total_posts(request, user_id):
    """
    Purpose: Returns total number of posts a user has.
    Input: user_id (mandatory) <int>
    :param request:
    :param user_id:
    :return: int
    """
    if is_authorized(request, user_id):
        posts = HackPost.objects.filter(author=user_id)
        return Response(len(posts))
    else:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Authentication failed. Please login",
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def feed(request, user_id):
    """
    Purpose: Returns the Timeline of the User.
    Input: user_id <int>
    Output: Post objects with all the posts.
    """
    if is_authorized(request, user_id):
        try:
            user = get_user_model().objects.filter(id=user_id).first()
            posts = HackPost.objects.filter(author=user)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            error = {
                "Error_code": status.HTTP_400_BAD_REQUEST,
                "Error_Message": "There are no posts to show",
            }
            logger.error(e)
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
    else:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Authentication failed. Please login",
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def users(request):
    """
    For debugging only.
    """
    if request.method == "GET":
        all_users = get_user_model().objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)
