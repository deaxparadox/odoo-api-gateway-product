from rest_framework import serializers
from .models import OrderLinesModel, OrderModel, OrderManager
from rest_framework.validators import UniqueValidator


class PaymentValidator:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        # if value % self.base != 0:
        #     message = 'This field must be a multiple of %d.' % self.base
        #     raise serializers.ValidationError(message)
        print(value) 

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
        
class OrderManagerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer()
    class Meta:
        model= OrderManager
        fields = ["id", 'orders', "payment_type"]
    
class OMUpdateSerializer(serializers.Serializer):
    payment_type = serializers.CharField()    
    
    def validate(self, attrs):
        payment_types = ["NUL", "COD", "UPI", "DEB"]
    
        payment_mode = attrs['payment_type']
        if len(payment_mode) > 3 or payment_mode not in payment_types or payment_mode == payment_types[0]:
            raise serializers.ValidationError("Invalid payment type.")

        return attrs
        