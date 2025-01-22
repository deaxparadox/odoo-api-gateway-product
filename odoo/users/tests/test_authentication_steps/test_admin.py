from django.test import TestCase
from django.contrib.auth.models import User
from users.models import ClientUserModel
from rest_framework.test import APIClient
import helpers


class TestAdmin(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        admin_auth_user = User.objects.create_superuser(username="admin", email="admin@email.com", password="136900")
        # admin_client_user = ClientUserModel.objects.create(
        #     user_id=helpers.create_variable_hash(admin_auth_user.email),
        #     auth_user=admin_auth_user
        # )
        # Superuser ClientUserModel instance is created using `post_save` signal,
        # see code in `users.models`
        admin_auth_user = admin_auth_user.client_user
        return super().setUp()

    def test_login_and_get_all_users(self):
        
        # Login
        response_login = self.api_client.post(
            "http://localhost:8000/api/auth/login/",
            data = {
                "username": "admin",
                "password": "136900"
            }
        )
        self.assertEqual(response_login.status_code, 200)
        
        # Get all users
        refresh = response_login.data.get("refresh")
        access = response_login.data.get("access")
        # self.api_client.headers.update({"Authorization": "Bearer %s" % access})
        response_users = self.api_client.get(
            "http://localhost:8000/api/users/",
            HTTP_AUTHORIZATION = "Bearer %s" % access
        )
        self.assertEqual(response_users.status_code, 200)