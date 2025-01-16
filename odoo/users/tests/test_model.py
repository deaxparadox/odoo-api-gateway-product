from django.test import TestCase
from django.contrib.auth.models import User
from users.models import ClientUserModel
import helpers

class UserCreateTest(TestCase):
    def test_new_user_creation(self):
        authuser = User.objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="136900"
        )
        clientuser = ClientUserModel.objects.create(
            user_id=helpers.create_variable_hash(authuser.email),
            auth_user=authuser
        )
    