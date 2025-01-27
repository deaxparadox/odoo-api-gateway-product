from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core import cache
from basket.models import BasketItem, BasketModel
from product.models import ProductVariantsModel
from helpers.permissions import OnlyUser
from .models import (
    OrderLinesModel, 
    OrderModel, 
    OrderStatus, 
    OrderManager, 
    PaymentChoices
)
from .serializers import (
    OrderSerializer,
    OrderDetailSerializer,
    OrderManagerSerializer,
    OMUpdateSerializer,
    OrderLineSerializer
)
from helpers.permissions import OnlyUser
from helpers.generate import generate_random_string

class OrderView(APIView):
    
    permission_classes = [IsAuthenticated, OnlyUser]
    
    def get(self, request):
        """
        Get all order
        
        fields:
        user_id: from request
        
        """
        try:
            client_user = request.user.client_user
            # if hasattr(client_user, 'order_manager'):
            #     orders: list[OrderManager] = []
            #     for item in client_user.order_manager.all():
            #         orders.append(OrderManagerSerializer(item).data)
            #     return Response({"Message": orders}, status=status.HTTP_200_OK)
            # return Response({"Message": "No order"}, status=status.HTTP_404_NOT_FOUND)
            
            data = {}
            orders = client_user.orders.all()
            serializer = OrderDetailSerializer(orders, many=True)
            return Response({"Message": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def generate_order_id(self):
        new_order_id = generate_random_string()
        while len(OrderModel.objects.filter(order_id=new_order_id)) > 0:
            new_order_id = generate_random_string()
        return new_order_id
    
    def generate_order_line_id(self):
        new_order_id = generate_random_string()
        while len(OrderLinesModel.objects.filter(line_id=new_order_id)) > 0:
            new_order_id = generate_random_string()
        return new_order_id
        
    def post(self, request):
        """
        Create a new order.
        
        Copy the basket information to generate order, and
        basket item information to generate order lines.
        
        
        - Get user from the request
        - Fetch basket using user.
        - Basket items will be convert to order 
        """
        
        try:
            client_user = request.user.client_user
            basket: BasketModel = client_user.basket
            basket_item: list[BasketItem] = basket.basket_item.all()
            
            if len(basket_item) == 0:
                return Response({"Error": "Empty basket, add product to the basket."}, status=status.HTTP_400_BAD_REQUEST)
            
            # check for incompleted (pending orders)
            # if pending order existing the notify the user to 
            # complete or delete the last order.
            if len(OrderManager.objects.filter(user_id=client_user.user_id)) > 0:
                order = OrderModel.objects.get(user_id=client_user.user_id)
                return Response({"Message": "You have incompleted order id %s, either discard it or complete the order" % order.order_id}, status=status.HTTP_302_FOUND)
            
            
            # update the price of basket and basket item
            basket.set_total_price()
            basket.save()
            
            # create order    
            new_order_id = self.generate_order_id()
            new_order = OrderModel.objects.create(
                order_id=new_order_id,  
                user_id=client_user,
                total_price = basket.total_price
            )
            
            # create order line, copy basket item to order line 
            for item in basket_item:
                new_order_line_id = self.generate_order_line_id()
                # Product variant
                variant: ProductVariantsModel = item.product_id
                order_line = OrderLinesModel(
                    line_id=new_order_line_id,
                    order_id=new_order,
                    product_id=item.product_id,
                    product_uom_qty=item.quantity,
                    price_unit = variant.get_total_price(),
                    subtotal=item.total_price
                )
                # Order approach, on creating the order, the qantity will be alotted to 
                # the user and will be on hold. Variant quantity from the database will be
                # deceased.
                # 
                # decrease the variant quantity in database and it.
                
                variant.sku-=item.quantity
                variant.save()
                # save the order line
                order_line.save()
                
            order_manager = OrderManager.objects.create(
                orders=new_order,
                user_id=client_user
            )
            
            serializer = OrderSerializer(new_order)
            return Response({"Message": serializer.data}, status=status.HTTP_201_CREATED)
               
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class OrderDetails(APIView):
    
    permission_classes = [IsAuthenticated, OnlyUser]
    
    def get(self, request, order_id):
        """
        Return the current order in process.
        """
        try:
            client_user = request.user.client_user
            print("calling right function")
            data = {}
            orders = client_user.orders.filter(order_id=order_id)
            if len(orders) == 0:
                return Response({"Error": "No order found"}, status=status.HTTP_404_NOT_FOUND)
            if len(orders) > 1:
                return Response({"Error": "Multiple order returned"}, status=status.HTTP_409_CONFLICT)
            order = orders[0]
            serializer = OrderDetailSerializer(order)
            serializer_order_line = OrderLineSerializer(order.order_line.all(), many=True)
            serializer_manager = OrderManagerSerializer(order.order_manager)
            data.update({"order": {**serializer.data}})
            data.update({"order_line": serializer_order_line.data})
            data.update({"payment": serializer_manager.data})
            
            return Response({"Message": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, order_id):
        """
        Update the order details.
        
        - Update the payment methods.
        """
        try:
            serializer = OMUpdateSerializer(data=request.data)
            if serializer.is_valid():
                order = OrderModel.objects.get(order_id=order_id)
                order_manager = order.order_manager
                order_manager.payment_type = serializer.validated_data.get("payment_type")
                order_manager.save()
                return Response({"Message": serializer.data}, status=status.HTTP_202_ACCEPTED)
            return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, order_id):
        """
        Delete the order.
        
        - Delete all order line objects.
        - Delete order object.
        - Delete related manager object.
        """
        try:
            order = OrderModel.objects.filter(user_id=request.user.client_user.user_id).filter(order_id=order_id)
            order_lines = OrderLinesModel.objects.filter(order_id=order_id)
            order_manager = OrderManager.objects.get(orders=order_id)
            order_manager.delete()
            for line in order_lines: line.delete()
            for o in order: o.delete()
            return Response({"Message": "Successfully deleted the order %s" % order_id}, status=status.HTTP_204_NO_CONTENT)
            # return Response({"Error": "Not order found with the following ID."})
                
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)