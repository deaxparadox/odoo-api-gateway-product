from django.contrib.auth.models import User
from django.test import TestCase
from .models import BasketModel
from users.models import ClientUserModel
from helpers.test import TestData
from helpers import create_variable_hash

class TestBasketModel(TestCase):
    
    def setUp(self):
        return super().setUp()
    
    def test_new_instance_with_default(self):
        """
        BasketModel: Testing new instance with defaults.
        """
        instance = BasketModel.objects.create()
        self.assertEqual(instance.id, 1)
        self.assertEqual(instance.total_price, 0.)
        self.assertEqual(instance.user_id, None)
        self.assertEqual(instance.line_ids, None)
    
    def test_new_instance_with_user(self):
        """
        BasketModel: Testing new instance with only user_id and rest to default.
        """
        auth_user = User.objects.create_user(username=TestData.username1, email=TestData.email1, password=TestData.password1)
        client_user = ClientUserModel.objects.create(user_id=create_variable_hash(TestData.email1), auth_user=auth_user)
        instance = BasketModel.objects.create(user=client_user)
        self.assertEqual(instance.user.user_id, client_user.user_id)