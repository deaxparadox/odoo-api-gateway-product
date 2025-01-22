from rest_framework import serializers

from .models import BasketModel


class BasketSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BasketModel
        fields = ['id', 'user', 'line_ids', 'total_price']