from rest_framework import serializers
from product import models

class ProductCategorySerializer(serializers.ModelSerializer):
    child_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.ProductCategoryModel
        fields = ['name', 'vendor_id', 'description', 'id', 'child_ids', "parent_id"]
        
class ProductCategoryUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    child_ids = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=models.ProductCategoryModel.objects.all())
    parent_id = serializers.PrimaryKeyRelatedField(required=False, queryset=models.ProductCategoryModel.objects.all())
    description = serializers.CharField(required=False)
    class Meta:
        model = models.ProductCategoryModel
        fields = ['name', 'description', "parent_id", "child_ids"]
        
            

class PCCreateSerializer(serializers.Serializer):
    """
    name: required
    vendor_id = required
    descriptor = optional
    parent_id = optional
    child_ids = item list is optional but empty list required 
    """
    
    name = serializers.CharField()
    vendor_id = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    parent_id = serializers.IntegerField(required=False)
    child_ids = serializers.ListField(allow_empty=True, child=serializers.IntegerField())
    
    def create(self, validated_data):
        print(validated_data.keys())
        child_ids = validated_data.pop("child_ids", None)
        parent_id = validated_data.pop("parent_id", None)
        description = validated_data.pop("description", None)
        
        instance = models.ProductCategoryModel(
            name=validated_data.get("name")
        )
        if isinstance(description, str):
            instance.description = description
        
        # parent_id must exist to add
        if isinstance(parent_id, int):
            parent_check = models.ProductCategoryModel.objects.filter(id=parent_id)
            if len(parent_check) == 0:
               raise ValueError("Parent with parent_id %s does not exists" % parent_id)
            else:
                instance.parent_id = parent_check[0]
                
        # for many-to-many to be added models instance must be saved,
        # if any childs doesnot exists, delete the instance
        instance.save()
        
        # child_ids must exist to add
        childs: list[models.ProductCategoryModel] = []
        if len(child_ids) > 0:
            try:
                for child in child_ids:
                    child_instance = models.ProductCategoryModel.objects.get(id=child)
                    childs.append(child_instance)
            except Exception as e:
                # raise exception here to be catched in view
                instance.delete()
                raise models.ProductCategoryModel.DoesNotExist(str(e))
            for child in childs:
                instance.child_ids.add(child.id)
        return instance

class PCCreateReturnSerializer(serializers.ModelSerializer):
    child_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.ProductCategoryModel
        fields = ["name", "vendor_id", "description", "id", "parent_id", "child_ids"]
    
            
class PCUpdateSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.ProductCategoryModel
        fields = ["name", "vendor_id", "description", "id", "parent_id"]
        