from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .helper import is_email_valid, user_data
from .models import Posts, UserDetail
from .serializers import MainRegisterSerializer, PostsSerializer, UserDetailSerializer


# Create your views here.
class PostsApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get request method
        return: all posts
        params: userid
        it returns all posts and if user id then returns posts
        of that user.
        """

        if request.data:
            try:
                posts = Posts.objects.filter(author=request.data["userid"])
                serializer = PostsSerializer(posts, many=True)
                return Response(
                    {"status": "success", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            except Posts.DoesNotExist:
                return Response(
                    {"status": "error", "data": "Post Not Found"},
                    status=status.HTTP_200_OK,
                )
        posts = Posts.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request):
        """post request method
        required_params: title,body,author(user id)
        creates new post.
        """
        serializer = PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        try:
            pid = request.data["id"]
            post = Posts.objects.get(id=pid)
            post_likes = post.likes.all()
            post_dislikes = post.unlikes.all()
            data = request.data
            data._mutable = True
            if "likes" in data:
                like_by = User.objects.get(id=data["likes"])
                if like_by in post_dislikes:
                    post.unlikes.remove(like_by)
                post.likes.add(like_by)
                data.pop("likes")
            if "unlikes" in data:
                dislike_by = User.objects.get(id=data["unlikes"])
                if dislike_by in post_likes:
                    post.likes.remove(dislike_by)

                post.unlikes.add(dislike_by)
                data.pop("unlikes")
            serializer = PostsSerializer(post, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "error", "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Posts.DoesNotExist:
            return Response(
                {"status": "error"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        try:
            pid = request.data["id"]
            post = Posts.objects.get(id=pid)
            post.delete()
            return Response(
                {"status": "success", "data": "Post Deleted"},
                status=status.HTTP_200_OK
            )
        except Posts.DoesNotExist:
            return Response(
                {"status": "error", "data": "Post not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RegistrationApi(APIView):
    serializer_class = MainRegisterSerializer

    def post(self, request):
        email = request.data["email"]
        email_check = is_email_valid(email)
        if type(email_check) == int:
            email_format, email_smtp = False, False
        else:
            email_format, email_smtp = email_check
        if email_format and email_smtp:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data.get("password")
                serializer.validated_data["password"] = make_password(password)
                username = serializer.validated_data.get("username")
                serializer.save()
                user = User.objects.get(username=username)
                user_data = user_data(email)
                user_detail = UserDetail.objects.create(
                    user=user,
                    city=user_data["city"],
                    country=user_data["country"],
                    country_code=user_data["country_code"],
                    is_holiday=user_data["is_holiday"],
                    holiday=user_data["holiday"],
                )
                user_detail.save()

                return Response(
                    {"status": "success"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": "error", "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {"status": "error", "data": "Email Invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_detail = UserDetail.objects.get(id=request.data["id"])
            serializer = UserDetailSerializer(user_detail)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"status": "error"}, status=status.HTTP_400_BAD_REQUEST
            )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.data = {"Success": "Login successfully", "data": data}
                return response
            else:
                return Response(
                    {"No active": "This account is not active!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Invalid": "Invalid username or password!!"},
                status=status.HTTP_404_NOT_FOUND,
            )
