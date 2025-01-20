from rest_framework import serializers
from product import models


class ProductCategorySerializer(serializers.ModelSerializer):
    child_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = models.ProductCategoryModel
        fields = "__all__"
        
class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategoryModel
        fields = ['name', 'vendor_id', 'description']
            
class PCCreateReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategoryModel
        fields = "__all__"
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)