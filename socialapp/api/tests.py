import json

import jwt
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .serializers import MainRegisterSerializer, PostsSerializer

jwt_options = {
        'verify_signature': False,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }
user_data = {
"username":"MrCodeGrapher",
            "email":"ahsansjobs@gmail.com",
            "password":"mypassword12345"
}

# Create your tests here.

# class RegistrationTestCase(APITestCase):
#     registration_url = reverse('registration')
#     def test_registration(self):
#         data = {
#             "username":"MrCodeGrapher",
#             "email":"ahsansjobs@gmail.com",
#             "password":"mypassword12345"
#             }
        
#         response = self.client.post(self.registration_url,data)
#         response.status_code ==200
    
    # def test2_registration(self):
    #     data = {
    #         "username":"MrCodeGrapher",
    #         "email":"abc@gmail.com",
    #         "password":"mypassword12345"
    #         }
        
    #     response = self.client.post(self.registration_url,data)
    #     response.status_code !=200

# class LoginTestCases(APITestCase):
#     registration_url = reverse('registration')
#     login_url = reverse('login')
#     def test_correct_credentials(self):
#         data = user_data 
#         self.client.post(self.registration_url,data)
#         response=self.client.post(self.login_url,{"username":"MrCodeGrapher","password":"mypassword12345"})
#         print(response.data)
#         response.status_code ==200

#     def test_Incorrect_credentials(self):
#         data = {
#             "username":"MrCodeGrapher",
#             "email":"ahsansjobs@gmail.com",
#             "password":"mypassword12345"
#             }
        
#         self.client.post(self.registration_url,data)
#         response=self.client.post(self.login_url,{"username":"MrCode","password":"mypassword12345"})
#         print(response.data)
#         response.status_code !=200


class PostsTestCases(APITestCase):
    posts_url = reverse('posts')
    registration_url = reverse('registration')
    login_url = reverse('login')
    
    def test_create_post(self):
        self.client.post(self.registration_url,user_data)
        response=self.client.post(self.login_url,{"username":"MrCodeGrapher","password":"mypassword12345"})
        auth_token = response.data['data']['access']
        print(auth_token)
        payload = jwt.decode(auth_token,'secret', algorithms=['HS256'],options=jwt_options)
        user_id = payload['user_id']
        print(user_id)

        data= {
        "title":"Test",
        "body":"This post is for Test",
        "author":user_id
        }
        header = {"Authorization": f"Bearer {auth_token}"}
        response= self.client.post(self.posts_url,data=data,headers=header)
        response.status_code==200
    
    def test_get_posts():
        pass


