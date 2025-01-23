from django.contrib.auth.models import User
from django.test import TestCase
from .models import BasketModel, BasketItem
from users.models import ClientUserModel
from product.models import ParentProductModel, ProductCategoryModel, ProductVariantsModel, AttributesModel
from helpers.test import TestData
from helpers import create_variable_hash
from helpers.generate import generate_uuid4


class TestBasketModel(TestCase):
    
    def test_new_instance_with_default(self):
        """
        BasketModel: Testing new instance with defaults.
        """
        instance1 = BasketModel.objects.create()
        self.assertEqual(instance1.id, 1)
        self.assertEqual(instance1.total_price, 0.)
        self.assertEqual(instance1.user_id, None)
        self.assertEqual(instance1.line_ids.all().__len__(), 0)
        
        instance2 = BasketModel.objects.create()
        self.assertEqual(instance2.id, 2)
        self.assertEqual(instance2.total_price, 0.)
        self.assertEqual(instance2.user_id, None)
        self.assertEqual(instance1.line_ids.all().__len__(), 0)
        
    
    def test_new_instance_with_user(self):
        """
        BasketModel: Testing new instance with only user_id and rest to default.
        """
        auth_user = User.objects.create_user(username=TestData.username1, email=TestData.email1, password=TestData.password1)
        client_user = ClientUserModel.objects.create(user_id=create_variable_hash(TestData.email1), auth_user=auth_user)
        instance = BasketModel.objects.create(user=client_user)
        self.assertEqual(instance.user.user_id, client_user.user_id)
    
    def test_basket_reverse_relation_to_client_user(self):
        """
        Testing the BasketModel backward relation to client_user
        """
        auth_user = User.objects.create_user(username=TestData.username1, email=TestData.email1, password=TestData.password1)
        client_user = ClientUserModel.objects.create(user_id=create_variable_hash(TestData.email1), auth_user=auth_user)
        instance = BasketModel.objects.create(user=client_user)
        # self.assertEqual(client_user.basket, client_user.user_id)
        self.assertEqual(type(client_user), ClientUserModel)
        self.assertEqual(type(client_user.basket), BasketModel)
    
    def test_basket_item(self):
        auth_user = User.objects.create_user(username=TestData.username1, email=TestData.email1, password=TestData.password1)
        client_user = ClientUserModel.objects.create(user_id=create_variable_hash(TestData.email1), auth_user=auth_user)
        basket = BasketModel.objects.create(user=client_user)
        # 
        product_category = ProductCategoryModel.objects.create(
            name="Hardware", 
            vendor_id="Hardware vendor",
            description="This is the first hardware vendor"
        )
        # 
        parent_product = ParentProductModel.objects.create(
            name="Jacket Hammer",
            list_price=1200,
            description="Jacket hammer using for digging hole and breaking stuff"
        )
        parent_product.tags.add("hardware", "hammer")
        parent_product.category_ids.add(product_category)
        # 
        parent_variant = ProductVariantsModel.objects.create(
            sku=100, barcode=generate_uuid4(), price_extra=100
        )
        parent_variant.product_template_id.add(parent_product)
        # attr_value1 = parent_variant.attribute_values.create(name="Red")
        # attr_value2 = parent_variant.attribute_values.create(name="Blue")
        attr = AttributesModel.objects.create(name="Color", type="radio")
        attr_value1 = attr.values.create(name="Red")
        attr_value2 = attr.values.create(name="Blue")
        parent_variant.attribute_values.add(attr_value1)
        parent_variant.attribute_values.add(attr_value2)
        
        # 
        basket_item = BasketItem.objects.create(basket_id=basket, product=parent_product)
        # basket.basket_item.create(product=parent_product)
        # attr_value1.attribute_id = attr
        # attr_value1.save()
        # attr_value2.attribute_id = attr
        # attr_value2.save()
        # 