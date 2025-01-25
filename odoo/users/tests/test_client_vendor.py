from django.test import TestCase
from django.contrib.auth.models import User
from users.models import VendorsModel, AddressModel
from helpers.test import TestData
from helpers import create_variable_hash

def create_user():
    user = User.objects.create(
        username=TestData.User.username1,
        email=TestData.User.email1,
        password=TestData.User.password
    )
    return user

def create_client_user(user: User):
    client_user = VendorsModel(
        auth_user=user,
        user_id=create_variable_hash(user.email)
    )
    return client_user

class TestClientUser(TestCase):
    def setUp(self):
        return super().setUp()
    def tearDown(self):
        return super().tearDown()
    
    def test_new_instance(self):
        user: User = create_user()
        client_user: VendorsModel = create_client_user(user)
        self.assertEqual(client_user.user_id, create_variable_hash(user.email))
        self.assertEqual(client_user.auth_user.id, user.id)

    def test_client_user_address(self):
        user = User.objects.create(
            username=TestData.User.username2,
            email=TestData.User.email2,
            password=TestData.User.password
        )
        client_user = VendorsModel.objects.create(
            auth_user=user,
            user_id=create_variable_hash(user.email)
        )
        address = AddressModel.objects.create(
            address1=TestData.Address.address, 
            state=TestData.Address.state,
            country=TestData.Address.country
        )
        address.user_id = client_user
        address.save()
