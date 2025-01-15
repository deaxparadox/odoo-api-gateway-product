from django.db import models
from django.utils.translation import gettext_lazy as _

class ProductCategory(models.Model):
    id = models.CharField(
        max_length=10, 
        verbose_name="Unique identifier of the category",
        primary_key=True
    )
    name = models.CharField(max_length=120, verbose_name="Name of the category")
    vendor_id = models.CharField(max_length=120, verbose_name="The product owner")
    parent_id = models.CharField(max_length=120, verbose_name="ID of the parent Category")
    # child_ids = models.ForeignKey(
    #     "self",
    #     on_delete=
    # )
    description = models.TextField(verbose_name="Description of the category")
    
class ParentProduct(models.Model):
    id = models.CharField(
        max_length=10, 
        verbose_name="Unique identifier of the category",
        primary_key=True
    )
    name = models.CharField(max_length=120, verbose_name="Project name")
    category_ids = models.CharField(max_length=10, verbose_name="Category IDs of the products belongs to")
    list_price = models.FloatField(default=0.0, verbose_name="Default price of the project")
    description = models.TextField(verbose_name="Long description")
    image_url = models.URLField(verbose_name="URL of the project's image")
    # tags = mode

class ProductVariants(models.Model):
    id = models.CharField(
        max_length=10, 
        verbose_name="Unique identifier of the variant",
        primary_key=True
    )
    product_template_id = models.CharField(max_length=10, verbose_name="ID of the parent product tempate")
    # attribute_values = models.ForeignKey(Attributes)  
    sku = models.CharField(max_length=120, blank=True, null=True, verbose_name="Stock Keeping Unit, if application")
    barcode = models.CharField(
        max_length=120,
        verbose_name="Barcode of the project"
    )
    price_extra = models.FloatField(
        default=0.0,
        verbose_name="Price difference from the base project template price"
    )


class AttributesCustom(models.Model):
    NULL = "NUL", _("Null")
    CUSTOM = "CUS", _("Custom")
    PREDEFINED = "PRE", _("Predefined")
    


class Atributes(models.Model):
    id = models.CharField(
        max_length=10, 
        verbose_name="Unique identifier of the attribute",
        primary_key=True
    )
    name = models.CharField(max_length=120, verbose_name="Name of the attribute")
    type = models.CharField(max_length=15, verbose_name="Type of the attribute")
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.NULL
    )
    # value_ids = 
    

class AttributeValues(models.Model):
    id = models.CharField(
        max_length=120,
        verbose_name="Unique identifier of the attribute value",
        primary_key=True
    )
    name = models.CharField(max_length=120, verbose_name="Name of the attribute value")
    attribute_id = models.CharField(max_length=10, verbose_name="ID of the parent attribute")
    # sequence = 
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.NULL
    )
    


