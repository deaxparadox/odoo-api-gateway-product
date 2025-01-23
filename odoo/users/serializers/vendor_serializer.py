from rest_framework import serializers
from users.models import VendorsModel


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorsModel
        fields = ['id', 'name', 'email', 'phone', 'address', 'is_compnay', 'active']