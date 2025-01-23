from django.test import TestCase
from product import models
from helpers.generate import generate_rand_number_from, generate_uuid4

class TestProductVariant(TestCase):
    def test_new_instance(self):
        instance = models.ProductVariantsModel.objects.create(
            # sku=generate_uuid4(), 
            barcode=generate_uuid4(), 
            price_extra=generate_rand_number_from(500., 100.)
        )
        
    def test_new_instance_add_product_template_relation(self):
        # {
        #     "id": 5,
        #     "name": "Shirt2",
        #     "category_ids": [],
        #     "list_price": 11220.0,
        #     "image_url": null,
        #     "description": "something to describe"
        # }
        instance = models.ProductVariantsModel.objects.create(
            # sku=generate_uuid4(), 
            barcode=generate_uuid4(), 
            price_extra=generate_rand_number_from(500., 1000.)
        )
        instance.product_template_id.create(
            name="shirt", 
            list_price=generate_rand_number_from(500., 1000.,),
            description="Shirt type"
        )
        pre_id = instance.id
        cur = models.ProductVariantsModel.objects.get(id=pre_id)
        self.assertEqual(len(cur.product_template_id.all()), 1)
        
    def test_new_instance_add_attributes_relation(self):
        instance = models.ProductVariantsModel.objects.create(
            # sku=generate_uuid4(), 
            barcode=generate_uuid4(), 
            price_extra=generate_rand_number_from(500., 1000.)
        )
        instance.attribute_values.create(
            name="Color",
        )
        pre_id = instance.id
        cur = models.ProductVariantsModel.objects.get(id=pre_id)
        self.assertEqual(len(cur.attribute_values.all()), 1)
        
    def test_new_instance_add_all_relation(self):
        instance = models.ProductVariantsModel.objects.create(
            # sku=generate_uuid4(), 
            barcode=generate_uuid4(), 
            price_extra=generate_rand_number_from(500., 1000.)
        )
        instance.product_template_id.create(
            name="shirt", 
            list_price=generate_rand_number_from(500., 1000.,),
            description="Shirt type"
        )
        instance.attribute_values.create(
            name="Color",
        )
        pre_id = instance.id
        cur = models.ProductVariantsModel.objects.get(id=pre_id)
        self.assertEqual(len(cur.attribute_values.all()), 1)
        self.assertEqual(len(cur.product_template_id.all()), 1)
    
    
    def test_new_instance_add_attribute_relation_custom_custom(self):
        instance = models.ProductVariantsModel.objects.create(
            # sku=generate_uuid4(), 
            barcode=generate_uuid4(), 
            price_extra=generate_rand_number_from(500., 1000.)
        )
        instance.product_template_id.create(
            name="shirt", 
            list_price=generate_rand_number_from(500., 1000.,),
            description="Shirt type"
        )
        instance.attribute_values.create(
            name="Color",
            is_custom=models.AttributesCustom.CUSTOM
        )
        pre_id = instance.id
        cur = models.ProductVariantsModel.objects.get(id=pre_id)
        self.assertEqual(len(cur.attribute_values.all()), 1)
        self.assertEqual(len(cur.product_template_id.all()), 1)
        self.assertEqual(cur.attribute_values.first().is_custom, models.AttributesCustom.CUSTOM)
        
    
    def test_new_instance_add_attribute_relation_custom_predefined(self):
        instance = models.ProductVariantsModel.objects.create(
            # sku=generate_uuid4(), 
            barcode=generate_uuid4(), 
            price_extra=generate_rand_number_from(500., 1000.)
        )
        instance.product_template_id.create(
            name="shirt", 
            list_price=generate_rand_number_from(500., 1000.,),
            description="Shirt type"
        )
        instance.attribute_values.create(
            name="Color",
            is_custom=models.AttributesCustom.PREDEFINED
        )
        pre_id = instance.id
        cur = models.ProductVariantsModel.objects.get(id=pre_id)
        self.assertEqual(len(cur.attribute_values.all()), 1)
        self.assertEqual(len(cur.product_template_id.all()), 1)
        self.assertEqual(cur.attribute_values.first().is_custom, models.AttributesCustom.PREDEFINED)
    