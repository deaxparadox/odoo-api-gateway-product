from rest_framework import serializers

from .models import BasketModel
from product.models import ProductCategoryModel, ProductVariantsModel
from product.serializers.pp_serializers import ParentProductModel


class BasketVariantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product_template_id = serializers.PrimaryKeyRelatedField(read_only=True)
    attribute_values = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = ProductVariantsModel
        fields = ["id", 'product_template_id', 'attribute_values']
        

class BasketSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BasketModel
        fields = ['id', 'user', 'total_price']
        
class BasketCreateSerializer(serializers.ModelSerializer):
    line_ids = serializers
    class Meta:
        model = BasketModel
        fields = ['id', 'user', 'total_price']
    
class BasketItemAddSerializers(serializers.Serializer):
    product_template_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # class Meta:
    #     model = ProductVariantsModel
    #     fields = ['product_template_id', 'quantity']
        

class BasketQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    basket_item_id = serializers.IntegerField()