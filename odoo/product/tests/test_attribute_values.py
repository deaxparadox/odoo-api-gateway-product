from django.test import TestCase
from product.models import (
    AttributeValuesModel, AttributesCustom,
    AttributesModel
)


class TestAttributeValuesModel(TestCase):
    def test_new_instance(self):
        """
        ### Testing : creating a new instance of AttributeValueModel
        """
        instance = AttributeValuesModel.objects.create(name="Red")
        self.assertEqual(instance.attribute_id, None)
        self.assertEqual(instance.sequence, 1)
        self.assertEqual(instance.is_custom, AttributesCustom.PREDEFINED)
        
    def test_new_instance_with_attribute_id(self):
        instance_attr = AttributesModel.objects.create(
            name='Color', type='radio',
            is_custom=AttributesCustom.PREDEFINED
        )
        instance = AttributeValuesModel.objects.create(name="Red", attribute_id=instance_attr)
        self.assertEqual(instance.attribute_id.id, instance_attr.id)
        self.assertEqual(instance.sequence, 1)
        self.assertEqual(instance.is_custom, AttributesCustom.PREDEFINED)
    
    def test_pre_save_signal(self):
        """
        ### Testing pre_save signal for setting AttributeValueModel.sequence fields ->
        """
        instance1 = AttributeValuesModel.objects.create(name="Red")
        self.assertEqual(instance1.attribute_id, None)
        self.assertEqual(instance1.sequence, 1)
        self.assertEqual(instance1.is_custom, AttributesCustom.PREDEFINED)
        
        instance2 = AttributeValuesModel.objects.create(name="Blue")
        self.assertEqual(instance2.attribute_id, None)
        self.assertEqual(instance2.sequence, 2)
        self.assertEqual(instance2.is_custom, AttributesCustom.PREDEFINED)
        
        instance3 = AttributeValuesModel.objects.create(name="Blue")
        self.assertEqual(instance3.attribute_id, None)
        self.assertEqual(instance3.sequence, 3)
        self.assertEqual(instance3.is_custom, AttributesCustom.PREDEFINED)
        
    def test_get_value_of_specific_category(self):
        """
        ### Testing : get all value of specific value category -> 
        """
        instance_attr = AttributesModel.objects.create(
            name='Color', type='select',
            is_custom=AttributesCustom.PREDEFINED
        )
        instance_attr.values.create(name="Red", attribute_id=instance_attr)
        all_values = instance_attr.values.all()
        self.assertEqual(len(all_values), 1)