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
from users.models import HackUser
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
)

EXP_TIME = datetime.timedelta(hours=2)


@api_view(["POST"])
def register(request):
    """
    Purpose: Create a new user
    Input:
    username (mandatory) <str> Chosen Username
    password (mandatory) <str> Chosen Password
    Output: User object of the created user
    """
    serializer = UserSerializer(data=request.query_params)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response("User was not created", status=status.HTTP_400_BAD_REQUEST)


def get_token(username):
    """
    Purpose: Get Access token
    Input:
    username (mandatory) <str> Account user
    password (mandatory) <str> Password
    Output: Token that expires in 60 minutes
    """
    try:
        user = HackUser.objects.get(username=username)
        if user:
            try:
                payload = {
                    "id": user.id,
                    "username": user.username,
                    "exp": datetime.datetime.utcnow() + EXP_TIME,
                }
                token = {"token": jwt.encode(payload, settings.AUTH_TOKEN)}
                # token = {
                # 'token': jwt.encode(
                # payload, settings.AUTH_TOKEN
                # ).decode('utf8')
                # }
                # jwt.encode({'exp': datetime.utcnow()}, 'secret')
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
                "Error_Message": "Invalid Username or Password",
            }
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Internal Server Error",
        }
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request, username=None, password=None):
    """
    Authenticate if username and password are correct.
    Input: username and password
    Output: return User object or Error
    """
    username = request.query_params.get("username")
    password = request.query_params.get("password")
    try:
        user = HackUser.objects.get(username=username)
        if user.password == password:
            token = get_token(username)
            user.token = token["token"]
            user.save()
            request.session["authtoken"] = token
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                "Error_code": status.HTTP_400_BAD_REQUEST,
                "Error_Message": "Invalid Username or Password",
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
    """ """
    try:
        user = HackUser.objects.get(id=user_id)
        user.token = ""
        user.save()
        request.session["authtoken"] = ""
        return Response("Successful logout.", status=status.HTTP_200_OK)

    except Exception as e:
        error = {
            "Error_code": status.HTTP_400_BAD_REQUEST,
            "Error_Message": "Invalid User ID",
        }
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


def authentication(request, username):
    """
    Purpose: Login to the Application
    Input:
    token (mandatory) <str> user token
    Output: User object of the logged in user
    """
    try:
        token = request.session.get("authtoken").get("token")
        payload = jwt.decode(token, settings.AUTH_TOKEN)
        user = HackUser.objects.get(username=username)
        if payload.get("username") == user.username:
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


def is_authorized(request, username):
    """
    Authorizing the user.
    :param request:
    :param username:
    :return:
    """
    validation = authentication(request, username)
    if validation.status_code == 200:
        return True  # Todo
    else:
        return False


@api_view(["PUT"])
def update_account(request, user_id):
    """
    Update Account Details.
    Input:
    user_id (mandatory) <int>
    name (optional) <str>
    description (optional) <str>
    photo (optional) <str>
    Output: User object of the updated user
    """
    try:
        user = HackUser.objects.get(id=user_id)
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


@api_view(["GET"])
def total_likes(request, user_id):
    """
    Purpose: Returns total number of likes a user has.
    Input: user_id (mandatory) <int>
    :param user_id:
    :return: str
    """
    posts = HackPost.objects.filter(author=user_id).aggregate(Sum("likes"))
    sum_likes = posts["likes__sum"]
    return Response(f"{sum_likes}")  # Todo None vs 0


# @api_view(['PUT'])
# def FollowUser(request, loggedin_user, user):
#     '''
#     Purpose: Follow the user
#     Input: -
#     Output: User object of the logged in user
#     '''
#     try:
#         cur_user = HackUser.objects.get(username=loggedin_user)
#         fol_user = HackUser.objects.get(username=user)
#         cur_user.following.add(fol_user)
#         cur_user.save()
#         serializer = UserSerializer(cur_user)
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         error = {'Error_code': status.HTTP_400_BAD_REQUEST,
#                  'Error_Message': "Request Failed. Invalid Details"}
#         logger.error(e)
#         return Response(error, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def GetFollowers(request, username):
#     '''
#     Purpose: Get all the followers for the user
#     Input: -
#     Output: User object of all the following users
#     '''
#     try:
#         user = HackUser.objects.get(username=username)
#         followers = user.followers.all()
#         serializer = UserSerializer(followers, many=True)
#         return Response(serializer.data)
#     except Exception as e:
#         error = {'Error_code': status.HTTP_400_BAD_REQUEST,
#                  'Error_Message': "User does not exist"}
#         logger.error(e)
#         return Response(error, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def GetFollowing(request, username):
#     '''
#     Purpose: Get all the users the given user is following
#     Input: -
#     Output: User object of all the followed users
#     '''
#     try:
#         user = HackUser.objects.get(username=username)
#         following = user.following.all()
#         serializer = UserSerializer(following, many=True)
#         return Response(serializer.data)
#     except Exception as e:
#         error = {'Error_code': status.HTTP_400_BAD_REQUEST,
#                  'Error_Message': "User does not exist"}
#         logger.error(e)
#         return Response(error, status=status.HTTP_400_BAD_REQUEST)

#
# @api_view(['PUT'])
# def Block_user(request, username):
#     '''
#     Purpose: Block the user
#     Input: -
#     Output: Blocked user
#     '''
#     try:
#         user = HackUser.objects.get(username=username)
#         user.blocked = True
#         user.save()
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         error = {'Error_code': status.HTTP_400_BAD_REQUEST,
#                  'Error_Message': "User does not exist"}
#         logger.error(e)
#         return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])  # Todo
def timeline(request, user_id):
    """
    Purpose: Returns the Timeline of the User in a Paginated Fashion
    Input: page (mandatory) <int>
    Output: Tweet object with all the tweets in the page
    """
    if not is_authorized(request, user_id):  # Todo
        try:
            posts = HackPost.objects.filter(author=user_id)
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
    Debugging
    """
    if request.method == "GET":
        users = HackUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
