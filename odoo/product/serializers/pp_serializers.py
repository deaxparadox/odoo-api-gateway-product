from rest_framework import serializers
from product.models import ParentProductModel

class PPSerializers(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = ParentProductModel
        fields = [
            "id",
            'name', 
            'category_ids', 
            "list_price",
            "image_url",
            "description",
        ]
        
class PPCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_null=True, required=False)
    class Meta:
        model = ParentProductModel
        fields = [
            'name', 
            'category_ids', 
            "list_price",
            "image_url",
            "description"
        ]
        
class PPCreateReturnSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = ParentProductModel
        fields = [
            "id",
            'name',
            'category_ids', 
            "list_price",
            "image_url",
            "description"
        ]