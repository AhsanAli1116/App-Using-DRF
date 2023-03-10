import jwt
from django.urls import reverse
from rest_framework.test import APITestCase

jwt_options = {
    "verify_signature": False,
    "verify_exp": True,
    "verify_nbf": False,
    "verify_iat": True,
    "verify_aud": False,
}
user_data = {
    "username": "MrCodeGrapher",
    "email": "ahsansjobs@gmail.com",
    "password": "mypassword12345",
}

auth_token = None
post_id = None
# Create your tests here.


class RegistrationTestCase(APITestCase):
    """ Test class for Registration test."""

    registration_url = reverse("registration")

    def test_registration(self):
        """Registration test With correct email."""

        data = {
            "username": "MrCodeGrapher",
            "email": "ahsansjobs@gmail.com",
            "password": "mypassword12345",
        }

        response = self.client.post(self.registration_url, data)
        response.status_code == 200

    def test2_registration(self):
        """Registration test With incorrect email."""

        data = {
            "username": "MrCodeGrapher",
            "email": "abc@gmail.com",
            "password": "mypassword12345",
        }

        response = self.client.post(self.registration_url, data)
        response.status_code != 200


class LoginTestCases(APITestCase):
    """Test Class Login tests"""

    registration_url = reverse("registration")
    login_url = reverse("login")

    def test_correct_credentials(self):
        """Login test with valid username and password"""

        data = user_data
        self.client.post(self.registration_url, data)
        response = self.client.post(
            self.login_url, {
                "username": "MrCodeGrapher",
                "password": "mypassword12345"
            }
        )
        global auth_token
        auth_token = response.data["data"]["access"]
        response.status_code == 200

    def test_Incorrect_credentials(self):
        """Login test with inValid username. """

        response = self.client.post(
            self.login_url, {
                "username": "MrCode",
                "password": "mypassword12345"
            }
        )
        response.status_code != 200

    def test2_Incorrect_credentials(self):
        """Login test with inValid Password. """

        response = self.client.post(
            self.login_url, {
                "username": "MrCodeGrapher",
                "password": "my12345password"
            }
        )
        response.status_code != 200


class PostsTestCases(APITestCase):
    """Test class for Post CRUD Operations"""

    posts_url = reverse("posts")
    registration_url = reverse("registration")
    login_url = reverse("login")

    def test_create_post(self):
        """Test creating new post."""

        global auth_token
        payload = jwt.decode(
            auth_token, "secret", algorithms=["HS256"], options=jwt_options
        )
        user_id = payload["user_id"]
        data = {
            "title": "Test",
            "body": "This post is for Test",
            "author": user_id
        }
        header = {"Authorization": f"Bearer {auth_token}"}
        response = self.client.post(self.posts_url, data=data, headers=header)
        global post_id
        response.status_code == 200

    def test_getall_posts(self):
        """Test accessing all posts."""

        global auth_token
        header = {"Authorization": f"Bearer {auth_token}"}
        response = self.client.get(self.posts_url, headers=header)
        response.status_code == 200

    def test_get_post_by_userId(self):
        """Test accessing Post by user Id"""

        global auth_token
        payload = jwt.decode(
            auth_token, "secret", algorithms=["HS256"], options=jwt_options
        )
        user_id = payload["user_id"]
        header = {"Authorization": f"Bearer {auth_token}"}
        response = self.client.get(
            self.posts_url, data={"id": user_id}, headers=header
        )
        response.status_code == 200

    def test_like_post(self):
        """Test for liking a post. """

        global auth_token, post_id
        payload = jwt.decode(
            auth_token, "secret", algorithms=["HS256"], options=jwt_options
        )
        user_id = payload["user_id"]
        header = {"Authorization": f"Bearer {auth_token}"}
        response = self.client.put(
            self.posts_url, data={"id": 1, "likes": user_id}, headers=header
        )
        response.status_code == 200

    def test_unlike_post(self):
        """Test for disliking a post. """

        global auth_token
        payload = jwt.decode(
            auth_token, "secret", algorithms=["HS256"], options=jwt_options
        )
        user_id = payload["user_id"]
        header = {"Authorization": f"Bearer {auth_token}"}
        response = self.client.put(
            self.posts_url, data={"id": 1, "unlikes": user_id}, headers=header
        )
        response.status_code == 200

    def test_delete_post(self):
        """Test for deleting a post."""

        global auth_token
        header = {"Authorization": f"Bearer {auth_token}"}
        response = self.client.delete(
            self.posts_url, data={"id": 1}, headers=header
        )
        response.status_code == 200
