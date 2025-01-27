from django.test import TestCase
from django.contrib.auth.models import User
from .models import OrderModel, OrderLinesModel, OrderStatus
from basket.models import BasketItem, BasketModel
from product.models import (
    ProductCategoryModel, 
    ProductVariantsModel, 
    ParentProductModel,
    AttributesModel,
    AttributeValuesModel
)
from users.models import (
    ClientUserModel,
    VendorsModel,
    AddressModel
)
from helpers.generate import generate_random_string, generate_uuid4
from helpers.test import TestData

class TestOrderModel(TestCase):
    def test_new_instance(self):
        auth_user_vendor = User.objects.create_user(
            username="testuser1",
            email="testuser1@email.com",
            password="136900"
        )
        auth_user_user = User.objects.create_user(
            username="testvendor1",
            email="testvendor1@email.com",
            password="136900"
        )
        client_vendor = VendorsModel.objects.create(
            user_id=generate_random_string(),
            auth_user=auth_user_vendor
        )
        client_user = ClientUserModel.objects.create(
            user_id=generate_random_string(),
            auth_user=auth_user_user
        )
        
        client_user_address_1 = AddressModel(
            address1=TestData.Address.address,
            state=TestData.Address.state,
            country=TestData.Address.country
        )
        client_user_address_1.user_id = client_user
        client_user_address_1.save()
        
        product_category = ProductCategoryModel.objects.create(
            name="Hardware",
            vendor_id=client_vendor
        )
        
        parent_product_1 = ParentProductModel.objects.create(
            name="Drill machine",
            list_price=1200.,
            description="Drill machine for drilling hole in walls",
        )
        parent_product_1.category_ids.add(product_category)
        parent_product_1.tags.add("hardware", "machine", "wall machine")
        
        parent_product_2 = ParentProductModel.objects.create(
            name="Grinder",
            list_price=1000.,
            description="Used for smoothing the surface",
        )
        parent_product_2.category_ids.add(product_category)
        parent_product_2.tags.add("hardware", "machine", "smoother")
        
        attribute_1 = AttributesModel.objects.create(
            name='Color',
            type="radio"
        )
        attribute_2 = AttributesModel.objects.create(
            name='Power',
            type="select"
        )
        
        attribute_value_1 = AttributeValuesModel.objects.create(
            name='Red',
            attribute_id = attribute_1
        )
        attribute_value_2 = AttributeValuesModel.objects.create(
            name='Brown',
            attribute_id = attribute_1
        )
        
        attribute_value_3 = AttributeValuesModel.objects.create(
            name='2000W',
            attribute_id = attribute_2
        )
        attribute_value_4 = AttributeValuesModel.objects.create(
            name='1000W',
            attribute_id = attribute_2
        )
        
        variant_1 = ProductVariantsModel.objects.create(
            product_template_id=parent_product_1,
            sku=100,
            barcode=generate_uuid4(),
            price_extra=200.
        )
        variant_1.attribute_values.add(attribute_value_1)
        variant_1.attribute_values.add(attribute_value_3)
        variant_2 = ProductVariantsModel.objects.create(
            product_template_id=parent_product_2,
            sku=100,
            barcode=generate_uuid4(),
            price_extra=300.
        )
        variant_2.attribute_values.add(attribute_value_2)
        variant_2.attribute_values.add(attribute_value_4)
        
        
        
        # creating a basket
        quantity = 2
        basket = BasketModel.objects.create(
            user=client_user
        )
        
        basket_item_1 = BasketItem.objects.create(
            basket_id=basket,
            product_id=variant_1, quantity=quantity
        )
        basket_item_1.set_total_price()
        basket_item_1.save()
        
        self.assertEqual(basket_item_1.total_price, 2800.)
        
        basket_item_2 = BasketItem.objects.create(
            basket_id=basket,
            product_id=variant_2, quantity=quantity
        )
        basket_item_2.set_total_price()
        basket_item_2.save()
        
        self.assertEqual(basket_item_2.total_price, 2600.)
        
        basket.set_total_price()
        basket.save()
        
        self.assertEqual(basket.total_price, 5400.)
        
        
        # quantity would not decrease until the product is ordered.
        order_instance = OrderModel(
            order_id=generate_random_string(),
            user_id=client_user,
            total_price=basket.total_price,
            shipping_address = client_user.address.all()[0]
        )
        order_instance.save()
        order_line_1 = OrderLinesModel.objects.create(
            line_id=generate_random_string(),
            order_id=order_instance,
            product_id=basket_item_1.product_id,
            product_uom_qty=basket_item_1.quantity,
            price_unit=basket_item_1.product_id.get_unit_price(),
            subtotal=basket_item_1.total_price
        )
        self.assertEqual(
            order_line_1.price_unit,
            basket_item_1.product_id.get_unit_price()
        )
        self.assertEqual(
            order_line_1.subtotal, 
            order_line_1.product_uom_qty * order_line_1.price_unit
        )
        
        order_line_2 = OrderLinesModel.objects.create(
            line_id=generate_random_string(),
            order_id=order_instance,
            product_id=basket_item_2.product_id,
            product_uom_qty=basket_item_2.quantity,
            price_unit=basket_item_2.product_id.get_unit_price(),
            subtotal=basket_item_2.total_price
        )
        self.assertEqual(
            order_line_2.price_unit,
            basket_item_2.product_id.get_unit_price()
        )
        self.assertEqual(
            order_line_2.subtotal, 
            order_line_2.product_uom_qty * order_line_2.price_unit
        )
        self.assertEqual(order_instance.status, OrderStatus.DRAFT)
        
        variant_1.sku-=quantity
        variant_1.save()
        self.assertEqual(variant_1.sku, 98)
        variant_2.sku-=quantity
        variant_2.save()
        self.assertEqual(variant_2.sku, 98)
        
        
        order_instance.status = OrderStatus.CONFIRMED
        order_instance.save()