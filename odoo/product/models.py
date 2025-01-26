from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from helpers.models import TimeIt
from taggit.managers import TaggableManager


# Product Category model
class ProductCategoryModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name=_("Name of the category"))
    vendor_id = models.ForeignKey(
        "users.VendorsModel",
        verbose_name=_("ID of the Vendor"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="product_category"
    )
    parent_id = models.ForeignKey(
        "self",
        verbose_name=_("ID of the parent Category"),
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="product_category"
    )
    child_ids = models.ManyToManyField(
        "self",
        verbose_name=_("List of child categories"),
        symmetrical=False
    )
    description = models.TextField(verbose_name=_("Description of the category"), null=True)
    active = models.BooleanField(default=True, verbose_name=_("Delete the category"))


# Product Template Model
class ParentProductModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name="Project name")
    category_ids = models.ManyToManyField(
        ProductCategoryModel,
        verbose_name="Category IDs of the products belongs to",
        related_name="parent_product"
    )
    list_price = models.FloatField(default=0.0, verbose_name="Default price of the project")
    description = models.TextField(verbose_name=_("Long description"), null=True, blank=True)
    image_url = models.URLField(default="https://", verbose_name="URL of the project's image", null=True)
    tags = TaggableManager()
    active = models.BooleanField(default=True, verbose_name=_("Delete a product"))

class AttributesCustom(models.TextChoices):
    CUSTOM = "CUS", _("Custom")
    PREDEFINED = "PRE", _("Predefined")
    
class AttributesIntegerChoices(models.IntegerChoices):
    PREDEFINED = 0
    CUSTOM = 1
    
    

class AttributeValuesModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name="Name of the attribute value")
    attribute_id = models.ForeignKey(
        "AttributesModel", 
        verbose_name=_("ID of the parent attribute"), 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="values"
    )
    sequence = models.IntegerField(default=0, verbose_name=_("Display order of the value"))
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.PREDEFINED
    )


class AttributesModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name="Name of the attribute")
    type = models.CharField(max_length=15, verbose_name="Type of the attribute")
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.PREDEFINED
    )
    value_ids = models.ForeignKey(
        AttributeValuesModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("List of possible values for the attribute"),
        related_name="attribute"
    )
    
class ProductVariantsModel(TimeIt):
    product_template_id = models.ForeignKey(
        ParentProductModel, 
        verbose_name=_("ID of the parent product template"), 
        related_name="product_variant",
        on_delete=models.SET_NULL,
        null=True
    )
    attribute_values = models.ManyToManyField(
        AttributeValuesModel, 
        verbose_name=_("Attributes assigned to the variant"), 
        related_name="product_variant"
    )  
    sku = models.IntegerField(default=0, verbose_name=_("Stock Keeping Unit, if application"))
    barcode = models.CharField(
        max_length=120,
        verbose_name="Barcode of the project"
    )
    price_extra = models.FloatField(
        default=0.0,
        verbose_name="Price difference from the base project template price"
    )
    
    def total_price(self):
        return self.price_extra + self.product_template_id.list_price


@receiver(pre_save, sender=AttributeValuesModel)
def set_sequence(sender, **kwrags):
    instance = kwrags['instance']
    last = AttributeValuesModel.objects.last()
    if not last:
        instance.sequence = 1
    else:
        cur = last.sequence
        cur+=1
        instance.sequence = cur
        