from rest_framework import serializers
from users.models import VendorsModel
from users.serializers import user_serializers


class VendorSerializer(serializers.ModelSerializer):
    auth_user = user_serializers.UserDetailSerializer()
    class Meta:
        model = VendorsModel
        fields = "__all__"
        
class VendorClientDetailSerializer(serializers.ModelSerializer):
    auth_user = user_serializers.UserDetailSerializer()
    
    class Meta:
        model = VendorsModel
        fields = ["user_id", "auth_user", "phone", "address"]