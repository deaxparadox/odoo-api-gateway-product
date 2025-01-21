from django.test import TestCase
from product.models import AttributesModel, AttributesCustom

class TestAttributesModel(TestCase):
    def test_create_new_instance(self):
        instance = AttributesModel(name="Color", type="", is_custom=AttributesCustom.NULL)
    
    