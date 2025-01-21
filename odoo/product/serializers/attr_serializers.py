from rest_framework import serializers
from product.models import AttributesModel, AttributeValuesModel

class AttrsSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    value_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = AttributesModel
        fields = ["id", 'name', 'type', "is_custom", 'value_ids']
        

class AttrsDetailSerializers(serializers.ModelSerializer):
    
    id = serializers.IntegerField(required=False)
    value_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=AttributeValuesModel.objects.all())
    class Meta:
        model = AttributesModel
        fields = ["id", 'name', 'type', "is_custom", 'value_ids']
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)