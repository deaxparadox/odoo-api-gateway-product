from rest_framework import serializers
from product.models import ParentProductModel, ProductCategoryModel

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
    description = serializers.CharField(required=False)
    category_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=ProductCategoryModel.objects.all())
    class Meta:
        model = ParentProductModel
        fields = [
            'name', 
            'category_ids', 
            "list_price",
            "image_url",
            "description"
        ]
        
class PPUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    image_url = serializers.URLField(required=False)
    list_price = serializers.CharField(required=False)
    category_ids = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=ProductCategoryModel.objects.all())
    class Meta:
        model = ParentProductModel
        fields = [
            'name', 
            'category_ids', 
            "list_price",
            "image_url",
            "description"
        ]
