from rest_framework import serializers
from .models import OrderLinesModel, OrderModel, OrderManager
from rest_framework.validators import UniqueValidator



class OrderSerializer(serializers.ModelSerializer):
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
        
class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLinesModel
        fields = ["line_id", "product_id", "product_uom_qty", "price_unit", "subtotal"]
        
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = [
            'order_id', 
            "name", 
            "user_id", 
            "status", 
            "order_date", 
            "total_price",
            "shipping_address",
        ]

        
class OrderManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderManager
        fields = ["payment_type"]
        

    
class OMUpdateSerializer(serializers.Serializer):
    payment_type = serializers.CharField()    
    
    def validate(self, attrs):
        payment_types = ["NUL", "COD", "UPI", "DEB"]
    
        payment_mode = attrs['payment_type']
        if len(payment_mode) > 3 or payment_mode not in payment_types or payment_mode == payment_types[0]:
            raise serializers.ValidationError("Invalid payment type.")

        return attrs
        