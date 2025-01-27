from rest_framework import serializers
from product.models import AttributesModel, AttributeValuesModel
from notifications.models import NotificationModel

class AttrsSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    value_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = AttributesModel
        fields = ["id", 'name', 'type', "is_custom", 'value_ids']
        


class AttrsCreateSerializers(serializers.Serializer):
    value_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    name = serializers.CharField(required=False)
    type = serializers.CharField()
    is_custom = serializers.CharField(required=False)

    def create(self, validated_data):
        instance = AttributesModel()
        
        name = validated_data.get("name", None)
        if name:
            instance.name = name
        # changing variable `type` to `attr_type`, 
        # it doesnot collied with python `type` object
        attr_type = validated_data.get('type', None)
        if attr_type:
            instance.type = attr_type
        is_custom = validated_data.get('is_custom', None)
        if is_custom:
            instance.is_custom = is_custom
        instance.save()
        value_ids_objs: list[AttributeValuesModel] = []
        value_ids = validated_data.get("value_ids")
        if isinstance(value_ids, list) and len(validated_data) > 0:
            for vids in value_ids:
                try:
                    value_ids_objs.append(AttributeValuesModel.objects.get(id=vids))
                except AttributeValuesModel.DoesNotExist as e:
                    # if any of the child doesn't exists,
                    # delete the newly created attribute instance
                    instance.delete()
                    raise AttributeValuesModel(str(e))
            for vids_obj in value_ids_objs:
                vids_obj.attribute_id = instance
                vids_obj.save()
    
        return instance

class AttrsDetailSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    value_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=AttributeValuesModel.objects.all())
    class Meta:
        model = AttributesModel
        fields = ["id", 'name', 'type', "is_custom", 'value_ids']
        
    def update(self, instance, validated_data):
        value_ids = validated_data.get("value_ids", None)
        if value_ids is None or isinstance(value_ids, list):
            validated_data.pop("value_ids")
        return super().update(instance, validated_data)
    
