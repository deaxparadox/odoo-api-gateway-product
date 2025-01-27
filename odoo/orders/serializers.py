from rest_framework import serializers
from .models import OrderLinesModel, OrderModel


class OrderSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    shipping_address = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = OrderModel
        fields = [
            'order_id', 
            "name", 
            "user_id", 
            "status", 
            "order_date", 
            "total_price",
            "shipping_address"
        ]