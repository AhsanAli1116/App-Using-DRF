from .helper import get_client_ip
from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import PostsSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Posts
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


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
class AllPosts(APIView):
    def get(self,request,id=None):
        if id:
            posts = Posts.objects.filter(author=id)
            serializer = PostsSerializer(posts,many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        posts = Posts.objects.all()
        serializer = PostsSerializer(posts, many=True)
        print("User IP" ,get_client_ip(request=request))
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
   
   


