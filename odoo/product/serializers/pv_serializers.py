from rest_framework import serializers
from product.models import ProductVariantsModel, ParentProductModel, AttributeValuesModel

class PVSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product_template_id = serializers.PrimaryKeyRelatedField(read_only=True)
    attribute_values = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = ProductVariantsModel
        fields = ["id", 'product_template_id', 'attribute_values', 'sku', 'barcode', 'price_extra']
        
    
class PVCreateSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product_template_id = serializers.PrimaryKeyRelatedField(queryset=ParentProductModel.objects.all())
    attribute_values = serializers.PrimaryKeyRelatedField(many=True, queryset=AttributeValuesModel.objects.all())
    class Meta:
        model = ProductVariantsModel
        fields = ["id", 'product_template_id', 'attribute_values', 'sku', 'barcode', 'price_extra']
    

class PVSerializersDetail(serializers.ModelSerializer):
    
    id = serializers.IntegerField(required=False)
    product_template_id = serializers.PrimaryKeyRelatedField(many=True, queryset=ParentProductModel.objects.all())
    attribute_values = serializers.PrimaryKeyRelatedField(many=True, queryset=AttributeValuesModel.objects.all())
    class Meta:
        model = ProductVariantsModel
        fields = ["id", 'product_template_id', 'attribute_values', 'sku', 'barcode', 'price_extra']
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)