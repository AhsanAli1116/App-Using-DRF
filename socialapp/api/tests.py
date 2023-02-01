import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .serializers import MainRegisterSerializer,PostsSerializer

# Create your tests here.

class RegistrationTestCase(APITestCase):
    registration_url = reverse('registration')
    def test_registration(self):
        data = {
            "username":"MrCodeGrapher",
            "email":"ahsansjobs@gmail.com",
            "password":"mypassword12345"
            }
        
        response = self.client.post(self.registration_url,data)
        response.status_code ==200
    
    def test2_registration(self):
        data = {
            "username":"MrCodeGrapher",
            "email":"abc@gmail.com",
            "password":"mypassword12345"
            }
        
        response = self.client.post(self.registration_url,data)
        response.status_code !=200

class LoginTestCases(APITestCase):
    registration_url = reverse('registration')
    login_url = reverse('login')
    def test_correct_credentials(self):
        data = {
            "username":"MrCodeGrapher",
            "email":"ahsansjobs@gmail.com",
            "password":"mypassword12345"
            }
        
        self.client.post(self.registration_url,data)
        response=self.client.post(self.login_url,{"username":"MrCodeGrapher","password":"mypassword12345"})
        print(response)
        response.status_code ==200

    def test_Incorrect_credentials(self):
        data = {
            "username":"MrCodeGrapher",
            "email":"ahsansjobs@gmail.com",
            "password":"mypassword12345"
            }
        
        self.client.post(self.registration_url,data)
        response=self.client.post(self.login_url,{"username":"MrCode","password":"mypassword12345"})
        print(response)
        response.status_code !=200


  

# class PostsTestCases(APITestCase):
#         all_posts_url = reverse('posts')

#         def create_post(self):

#         def get_all_posts(self):
#             response = self.client.get(self.all_posts_url)
#             response.status_code ==200
        
#         def get_posts(self):

