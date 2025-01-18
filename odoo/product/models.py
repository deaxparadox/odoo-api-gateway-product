from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.models import TimeIt


# Product Template Model
class ParentProduct(TimeIt):
    # id = models.CharField(
    #     max_length=10, 
    #     verbose_name="Unique identifier of the category",
    #     primary_key=True
    # )
    name = models.CharField(max_length=120, verbose_name="Project name")
    category_ids = models.CharField(max_length=10, verbose_name="Category IDs of the products belongs to")
    list_price = models.FloatField(default=0.0, verbose_name="Default price of the project")
    description = models.TextField(verbose_name="Long description")
    image_url = models.URLField(verbose_name="URL of the project's image", blank=True, null=True)
    # tags = mode

class ProductCategoryModel(TimeIt):
    # id = models.CharField(
    #     max_length=10, 
    #     verbose_name="Unique identifier of the category",
    #     primary_key=True
    # )
    name = models.CharField(max_length=120, verbose_name="Name of the category")
    vendor_id = models.CharField(max_length=120, verbose_name="The product owner")
    parent_id = models.ForeignKey(
        ParentProduct,
        on_delete=models.SET_NULL, 
        verbose_name="ID of the parent Category",
        null=True
    )
    child_ids = models.ManyToManyField(
        "self",
        verbose_name=_("List of child categories")
    )
    description = models.TextField(verbose_name="Description of the category")



class AttributesCustom(models.TextChoices):
    NULL = "NUL", _("Null")
    CUSTOM = "CUS", _("Custom")
    PREDEFINED = "PRE", _("Predefined")
    


class AttributeValues(TimeIt):
    # id = models.CharField(
    #     max_length=120,
    #     verbose_name="Unique identifier of the attribute value",
    #     primary_key=True
    # )
    name = models.CharField(max_length=120, verbose_name="Name of the attribute value")
    attribute_id = models.CharField(max_length=10, verbose_name="ID of the parent attribute")
    # sequence = 
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.NULL
    )
    

  

class ProductVariants(TimeIt):
    product_template_id = models.ManyToManyField(
        ParentProduct, 
        verbose_name=_("ID of the parent product template"), 
        related_name="product_variants"
    )
    attribute_values = models.ManyToManyField(
        AttributeValues, 
        verbose_name=_("Attributes assigned to the variant"), 
        related_name="product_variants"
    )  
    sku = models.CharField(max_length=120, blank=True, null=True, verbose_name="Stock Keeping Unit, if application")
    barcode = models.CharField(
        max_length=120,
        verbose_name="Barcode of the project"
    )
    price_extra = models.FloatField(
        default=0.0,
        verbose_name="Price difference from the base project template price"
    )




class Atributes(TimeIt):
    # id = models.CharField(
    #     max_length=10, 
    #     verbose_name="Unique identifier of the attribute",
    #     primary_key=True
    # )
    name = models.CharField(max_length=120, verbose_name="Name of the attribute")
    type = models.CharField(max_length=15, verbose_name="Type of the attribute")
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.NULL
    )
    value_ids = models.ManyToManyField(
        AttributeValues,
        verbose_name=_("List of possible values for the attribute"),
        related_name="attributes"
    )
    

