from rest_framework import serializers
from .models import Posts,UserDetail
from django.contrib.auth.models import User


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        # fields = ['id','title','body','author']
        fields ="__all__"

class MainRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {'password': {'write_only': True}}
        

class UserDetailSerializer(serializers.ModelSerializer):
    user = MainRegisterSerializer()
    class Meta:
        model = UserDetail
        fields = ["user","country","country_code","city","holiday"]