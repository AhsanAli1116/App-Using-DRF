from .helper import is_email_valid,user_data
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import PostsSerializer,MainRegisterSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Posts,UserDetail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
class PostsApi(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request,id=None):
        if id:
            posts = Posts.objects.filter(author=id)
            serializer = PostsSerializer(posts,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        posts = Posts.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK) 
    
    def post(self,request):
        serializer = PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pid = request.data['id']
        post = Posts.objects.get(id=pid)
        serializer = PostsSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,id):
        pid = request.data['id']
        post = Posts.objects.get(Posts, id=pid)
        post.delete()
        return Response({"status": "success", "data": "Post Deleted"})
   
   


class RegistrationApi(APIView):
    serializer_class = MainRegisterSerializer
    def post(self,request):
        # username=request.data['username']
        email = request.data['email']
        # password = request.data['password']
        email_check=is_email_valid(email)
        if len(email_check)==1:
            email_format,email_smtp=False
        else:
            email_format,email_smtp=email_check
        if email_format and email_smtp:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                password = serializer.validated_data.get('password')
                serializer.validated_data['password']=make_password(password)
                username=serializer.validated_data.get('username')
                serializer.save()
                user=User.objects.get(username=username)
                city,country,country_code,is_holiday,holiday=user_data(email)
                
                user_detail = UserDetail.objects.create(user=user,city=city,country=country,country_code=country_code,is_holiday=is_holiday,holiday=holiday)
                user_detail.save()

                return Response({"status": "success"},status=status.HTTP_200_OK)
            else:
                return Response({"status": "error" ,'data':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"status":'error','data': "Email Invalid"},status=status.HTTP_400_BAD_REQUEST)



