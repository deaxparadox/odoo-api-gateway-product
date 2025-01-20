from django.contrib import admin
from product import models

@admin.register(models.ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ParentProductModel)
class ParentProductAdmin(admin.ModelAdmin):
    pass

@admin.register(models.AttributeValuesModel)
class AttributeValuesAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductVariantsModel)
class ProductVariantAdmin(admin.ModelAdmin):
    # prepopulated_fields = ("attribute_id",)
    pass

@admin.register(models.AttributesModel)
class AttributesAdmin(admin.ModelAdmin):
    pass