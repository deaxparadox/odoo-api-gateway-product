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
    def test_add_parent_id(self):
        instance = ProductCategoryModel.objects.create(
            name='short', 
            vendor_id="New vendor",
            description="This is the test product short"
        )
        instance2 = ProductCategoryModel.objects.create(
            name='trouser',
            vendor_id="Another vendor",
            description="This is the trouser test product"
        )
        instance2.parent_id = instance
        instance2.save()
    def test_add_child_categories_id(self):
        pant = ProductCategoryModel.objects.create(
            name='pant', 
            vendor_id="New vendor",
            description="This is the test category pant"
        )
        short = ProductCategoryModel.objects.create(
            name='short', 
            vendor_id="New vendor",
            description="This is the test product short"
        )
        trouser = ProductCategoryModel.objects.create(
            name='trouser',
            vendor_id="Another vendor",
            description="This is the trouser test product"
        )
        pant.child_ids.add(short)
        pant.child_ids.add(trouser)
        pant_id = pant.id
        pant = ProductCategoryModel.objects.get(id=pant_id)
        self.assertEqual(len(pant.child_ids.all()), 2)