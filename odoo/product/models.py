from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from helpers.models import TimeIt
from taggit.managers import TaggableManager


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
    description = models.TextField(verbose_name=_("Description of the category"), null=True)
    active = models.BooleanField(default=True, verbose_name=_("Delete the category"))

    # def __repr__(self)
    def __str__(self) -> str:
        return "%s : %s" % (self.id, self.name)

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
    image_url = models.URLField(verbose_name="URL of the project's image", null=True)
    tags = TaggableManager()
    active = models.BooleanField(default=True, verbose_name=_("Delete a product"))

    def __str__(self) -> str:
        return "%s : %s" % (self.id, self.name)

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
    def __str__(self):
        return f"{self.id} : {self.name}"


class AttributesModel(TimeIt):
    name = models.CharField(max_length=120, verbose_name="Name of the attribute")
    type = models.CharField(max_length=15, verbose_name="Type of the attribute")
    is_custom = models.TextField(
        max_length=3,
        choices=AttributesCustom,
        default=AttributesCustom.PREDEFINED
    )
    value_ids = models.ManyToManyField(
        AttributeValuesModel,
        verbose_name=_("List of possible values for the attribute"),
        related_name="attributes"
    )
    
    def __str__(self):
        return f"{self.id} : {self.name}"

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
    
    def __str__(self):
        return f"{self.id} : {self.sku}"



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
        