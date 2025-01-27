from rest_framework import serializers
from product.models import (
    AttributesModel, 
    AttributeValuesModel,
    AttributesCustom
)

class AttributeValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # attribute_id = serializers.IntegerField(required=False)
    class Meta:
        model = AttributeValuesModel
        fields = ['id', 'name', "sequence", "is_custom", "attribute_id"]

class AVCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValuesModel
        fields = ['name', 'is_custom']
    
    def create(self, validated_data):
        instace = AttributeValuesModel.objects.create(
            name=validated_data.get('name'),
            is_custom=validated_data.get("is_custom")
        )
        instace.save()
        return instace
        
class AttributeValueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValuesModel
        fields = ['name',"is_custom"]
    
    def update(self, instance, validated_data):
        instance.name = validated_data.pop("name")
        instance.is_custom = validated_data.pop("is_custom")
        instance.save()
        return instance
        