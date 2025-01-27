from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from basket.models import BasketItem, BasketModel
from helpers.permissions import OnlyUser
from .models import OrderLinesModel, OrderModel, OrderStatus
from .serializers import OrderSerializer

class OrderView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get all order
        
        fields:
        user_id: from request
        
        """
        try:
            client_user = request.user.client_user
            if hasattr(client_user, 'orders'):
                return Response({"Message": "Order found"}, status=status.HTTP_200_OK)
            return Response({"Message": "No order"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)