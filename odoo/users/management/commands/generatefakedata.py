from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import call_command
from users.models import (
    VendorsModel, 
    ClientUserModel, 
    AddressModel
)
from django.contrib.auth.models import User
from product.models import (
    ProductCategoryModel, 
    ProductVariantsModel, 
    ParentProductModel, 
    AttributesCustom,
    AttributeValuesModel,
    AttributesModel
)
from basket.models import (
    BasketItem,
    BasketModel
)
from helpers import create_variable_hash
from helpers.test import TestData
from helpers.generate import generate_random_string, generate_uuid4

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true")

    def handle(self, *args, **options):
        if options['flush']:
            print("Flushing the database")
            call_command("flush")
            print("Loading the data")
            
        
        # create vendors
        # vendor 1
        vendor_user_1 = User.objects.create_user(username=TestData.Vendor.username1, email=TestData.Vendor.email1, password=TestData.Vendor.password)
        client_vendor_1 = VendorsModel.objects.create(auth_user=vendor_user_1, user_id=create_variable_hash(vendor_user_1.email))
        client_vendor_address_1 = AddressModel.objects.create(
            address1=TestData.Address.address,
            state=TestData.Address.state,
            country = TestData.Address.country
        )
        client_vendor_address_1.vendor_id = client_vendor_1
        client_vendor_address_1.save()
        Hardware = ProductCategoryModel.objects.create(
            name=TestData.ProductCateory.Hardware.name,
            description=TestData.ProductCateory.Hardware.description
        )
        Hardware.vendor_id = client_vendor_1
        Hardware.save()
         
         
        # vendor 2
        vendor_user_2 = User.objects.create_user(username=TestData.Vendor.username2, email=TestData.Vendor.email2, password=TestData.Vendor.password)
        client_vendor_2 = VendorsModel.objects.create(auth_user=vendor_user_2, user_id=create_variable_hash(vendor_user_2.email))
        client_vendor_address_2 = AddressModel.objects.create(
            address1=TestData.Address.address,
            state=TestData.Address.state,
            country = TestData.Address.country
        )
        client_vendor_address_2.vendor_id = client_vendor_2
        client_vendor_address_2.save()
        lock_category = ProductCategoryModel.objects.create(
            name=TestData.ProductCateory.Lock.name,
            description=TestData.ProductCateory.Lock.description
        )
        wheel_lock_category = ProductCategoryModel.objects.create(
            name=TestData.ProductCateory.WheelLock.name,
            description=TestData.ProductCateory.WheelLock.description
        )
        wheel_lock_category.parent_id = lock_category
        wheel_chain_lock_category = ProductCategoryModel.objects.create(
            name=TestData.ProductCateory.WheelChainLock.name,
            description=TestData.ProductCateory.WheelChainLock.description
        )
        wheel_chain_lock_category.parent_id = wheel_lock_category
        wheel_chain_lock_category.save()
        lock_category.child_ids.add(wheel_lock_category)
        lock_category.child_ids.add(lock_category)
        # product
        product_1 = ParentProductModel.objects.create(
            name="Primer wheel lock",
            list_price=1290.,
            image_url=TestData.url
        )
        product_1.category_ids.add(wheel_lock_category)
        product_1.category_ids.add(lock_category)
        product_1.tags.add("lock", "wheel")
        product_1.save()
        attribute_color = AttributesModel.objects.create(name=TestData.Attribute.Color.__name__)
        attribute_color_red = AttributeValuesModel.objects.create(
            name=TestData.Attribute.Color.RED.value[1],
            attribute_id=attribute_color
        )
        attribute_color_brown = AttributeValuesModel.objects.create(
            name=TestData.Attribute.Color.BROWN.value[1],
            attribute_id=attribute_color
        )
        attribute_color_golden = AttributeValuesModel.objects.create(
            name=TestData.Attribute.Color.GOLDEN.value[1],
            attribute_id=attribute_color
        )
        variant_1 = ProductVariantsModel.objects.create(
            product_template_id=product_1,
            sku=100,
            barcode=generate_uuid4(),
            price_extra=120
        )
        variant_1.attribute_values.add(attribute_color_brown)
        variant_1.attribute_values.add(attribute_color_golden)
        variant_1.attribute_values.add(attribute_color_red)
        variant_1.save()

        # create users
        # user 1
        user_1 = User.objects.create_user(
            username=TestData.User.username1, 
            email=TestData.User.email1, 
            password=TestData.User.password)
        client_user_1 = ClientUserModel.objects.create(auth_user=user_1, user_id=create_variable_hash(user_1.email))
        client_user_1_address_1 = AddressModel.objects.create(
            address1=TestData.Address.address,
            state=TestData.Address.state,
            country =  TestData.Address.country
        )
        client_user_1_address_1.user_id = client_user_1
        client_user_1_address_1.save()
         
        
        # user 2
        user_2 = User.objects.create_user(
            username=TestData.User.username2, 
            email=TestData.User.email2, 
            password=TestData.User.password
        )
        client_user_2 = ClientUserModel.objects.create(auth_user=user_2, user_id=create_variable_hash(user_2.email))
        client_user_2_address_1 = AddressModel.objects.create(
            address1=TestData.Address.address,
            state=TestData.Address.state,
            country =  TestData.Address.country
        )
        client_user_2_address_1.user_id = client_user_2
        client_user_2_address_1.save()
        
        # create first product
        ProductCategoryModel.objects.create(
            name=TestData.ProductCateory.Hardware.name,
            vendor_id=client_vendor_1
        )