from rest_framework import serializers

from .models import BasketModel
from product.models import ProductCategoryModel
from product.serializers.pp_serializers import ParentProductModel


class BasketSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BasketModel
        fields = ['id', 'user', 'line_ids', 'total_price']
        
class BasketCreateSerializer(serializers.ModelSerializer):
    line_ids = serializers
    class Meta:
        model = BasketModel
        fields = ['id', 'user', 'line_ids', 'total_price']
    