from rest_framework import serializers
from product import models


class ProductCategorySerializer(serializers.ModelSerializer):
    child_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = models.ProductCategoryModel
        fields = ['name', 'vendor_id', 'description', 'id', 'child_ids', "parent_id"]
        
class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategoryModel
        fields = ['name', 'vendor_id', 'description', "parent_id"]
            
class PCCreateReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategoryModel
        fields = ["name", "vendor_id", "description", "id", "parent_id"]
        
    def update(self, instance, validated_data, call_type: str = "update"):
        """
        Call update must be specified (either `update` or `create`), default to `update`
        """
        return super().update(instance, validated_data)
    
            
class PCUpdateSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.ProductCategoryModel
        fields = ["name", "vendor_id", "description", "id", "parent_id"]
        