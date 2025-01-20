from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.models import TimeIt


# Product Category model
class ProductCategoryModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name=_("Name of the category"))
    vendor_id = models.CharField(max_length=120, verbose_name=_("The product owner"))
    parent_id = models.OneToOneField(
        "self",
        verbose_name=_("ID of the parent Category"),
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    child_ids = models.ManyToManyField(
        "self",
        verbose_name=_("List of child categories")
    )
    description = models.TextField(verbose_name=_("Description of the category"))
    active = models.BooleanField(default=True, verbose_name=_("Delete the category"))

    # def __repr__(self)
    def __str__(self) -> str:
        return "%s" % (self.name)

# Product Template Model
class ParentProductModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name="Project name")
    category_ids = models.ManyToManyField(
        ProductCategoryModel, 
        verbose_name="Category IDs of the products belongs to",
        related_name="parent_product"
    )
    list_price = models.FloatField(default=0.0, verbose_name="Default price of the project")
    description = models.TextField(verbose_name="Long description")
    image_url = models.URLField(verbose_name="URL of the project's image", blank=True, null=True)
    # tags = mode

    def __str__(self) -> str:
        return "%s" % self.name

class AttributesCustom(models.TextChoices):
    NULL = "NUL", _("Null")
    CUSTOM = "CUS", _("Custom")
    PREDEFINED = "PRE", _("Predefined")
    


class AttributeValuesModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name="Name of the attribute value")
    attribute_id = models.CharField(max_length=10, verbose_name="ID of the parent attribute")
    # sequence = 
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.NULL
    )
    

  

class ProductVariantsModel(TimeIt):
    product_template_id = models.ManyToManyField(
        ParentProductModel, 
        verbose_name=_("ID of the parent product template"), 
        related_name="product_variants"
    )
    attribute_values = models.ManyToManyField(
        AttributeValuesModel, 
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




class AttributesModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name="Name of the attribute")
    type = models.CharField(max_length=15, verbose_name="Type of the attribute")
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.NULL
    )
    value_ids = models.ManyToManyField(
        AttributeValuesModel,
        verbose_name=_("List of possible values for the attribute"),
        related_name="attributes"
    )
    

