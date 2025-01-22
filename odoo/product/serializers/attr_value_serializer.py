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
        fields = ['id', 'name', 'attribute_id', "sequence", "is_custom"]