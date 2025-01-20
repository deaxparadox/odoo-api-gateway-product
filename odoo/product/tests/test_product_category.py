from django.test import TestCase
from product.models import ProductCategoryModel

class TestProductCategoryModel(TestCase):
    def test_create_new_object(self):
        instance = ProductCategoryModel.objects.create(
            name='short', 
            vendor_id="New vendor",
            description="This is the test product short"
        )
    def test_create_new_object_with_delete_flag(self):
        instance = ProductCategoryModel.objects.create(
            name='short', 
            vendor_id="New vendor",
            description="This is the test product short",
            active=False
        )
    def test_create_new_object(self):
        instance = ProductCategoryModel.objects.create(
            name='short', 
            vendor_id="New vendor",
            description="This is the test product short"
        )
    def test_create_new_object_and_delete(self):
        instance = ProductCategoryModel.objects.create(
            name='short', 
            vendor_id="New vendor",
            description="This is the test product short",
            active=False
        )
        instance.delete()
        