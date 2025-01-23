from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import BasketSerializer, BasketVariantSerializer, BasketQuantitySerializer
from .models import (
    BasketModel,
    BasketItem as BasketItemModel
)
from product.models import ProductVariantsModel
from product.serializers.pv_serializers import PVSerializers
from helpers.message import message_collector

def get_user_obj_from_jwt_request(request, /):
    token = str(request.auth)
    auth_user_id = AccessToken(token)['user_id']
    auth_user_obj = User.objects.get(id=auth_user_id)
    client_user_obj = auth_user_obj.client_user
    return auth_user_id, auth_user_obj, client_user_obj

class BasketView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        rmc = message_collector()
        try:
            *auth_user, client_user_obj = get_user_obj_from_jwt_request(request)
            # check basket existence
            if not hasattr(client_user_obj, "basket"):
                rmc("User's basket not found")
                return Response({
                    "Error": rmc(),
                }, status=status.HTTP_404_NOT_FOUND)
            queryset = client_user_obj.basket
            serializer = BasketSerializer(queryset)
            data = {**serializer.data}
            # Total value of basket
            basket_items = queryset.basket_item.all()
            data['total_price'] = sum(x.total_price() for x in basket_items)
            data['products'] = []
            for item in basket_items:
                pv_serializsers = BasketVariantSerializer(item.product_id)
                q = {
                    "quantity": item.quantity,
                    "basket_item_id": item.id
                }
                q.update({**pv_serializsers.data})
                # change variant referene from `id` to `product_variant_id`
                product_variant_id = q.pop("id")
                q.update({"product_variant_id": product_variant_id})
                # q.pop('price_extra')
                # q.pop("barcode")
                # q.pop("sku")
                data["products"].append(q)
            return Response({"Message": data}, status=status.HTTP_200_OK)
        except TokenError as e:
            rmc(str(e))
            return Response(
                {"Error": rmc()},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            rmc(str(e))
            return Response(
                {"Error": rmc()},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def post(self, request):
        rmc = message_collector()
        try:
            *auth_user, client_user_obj = get_user_obj_from_jwt_request(request)
            # check basket existence
            if not hasattr(client_user_obj, "basket"):
                basket = BasketModel.objects.create(user=client_user_obj)
                serializer = BasketSerializer(basket)
                rmc("Basket created successfully")
                return Response({"Message": [rmc()]}, status=status.HTTP_201_CREATED)
            
            # basket already exists
            rmc("User Basket exists")
            return Response({"Message": rmc()}, status=status.HTTP_302_FOUND)
        
        except Exception as e:
            rmc(str(e))
            return Response(
                {"Error": rmc()},
                status=status.HTTP_400_BAD_REQUEST
            )
            
class BasketItem(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # add item to the basket
        rmc = message_collector()
        
        try:
            *auth_user, client_user_obj = get_user_obj_from_jwt_request(request)
            pv_serializers = PVSerializers(data=request.data)
            if pv_serializers.is_valid():
                return Response(
                    {"Message": pv_serializers.data},
                    status=status.HTTP_202_ACCEPTED
                )
            # rmc(pv_serializers.data)
            return Response({"Error": pv_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            rmc(str(e))
            return Response({"Error": rmc()}, status=status.HTTP_400_BAD_REQUEST)
    
class BasketModifyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, basket_id):
        rmc = message_collector()
        
        try:
            quantity_serializer = BasketQuantitySerializer(data=request.data)
            if quantity_serializer.is_valid():
                *auth_user, client_user_obj = get_user_obj_from_jwt_request(request)
                # check basket existence
                if not hasattr(client_user_obj, "basket"):
                    rmc("User's basket not found")
                    return Response({
                        "Error": rmc(),
                    }, status=status.HTTP_404_NOT_FOUND)
                queryset = client_user_obj.basket
                
                # update basket
                basket_item = queryset.basket_item.get(id=basket_id)
                basket_item.quantity = quantity_serializer.validated_data['quantity']
                basket_item.save()
                
                # fetch data for display
                serializer = BasketSerializer(queryset)
                data = {**serializer.data}
                # Total value of basket
                basket_items = queryset.basket_item.all()
                data['total_price'] = sum(x.total_price() for x in basket_items)
                data['products'] = []
                for item in basket_items:
                    pv_serializsers = BasketVariantSerializer(item.product_id)
                    q = {
                        "quantity": item.quantity,
                        "basket_item_id": item.id
                    }
                    q.update({**pv_serializsers.data})
                    # change variant referene from `id` to `product_variant_id`
                    product_variant_id = q.pop("id")
                    q.update({"product_variant_id": product_variant_id})
                    data["products"].append(q)
                return Response({"Message": data}, status=status.HTTP_200_OK)
            return Response({"Error": quantity_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            rmc(str(e))
            return Response({"Error": rmc()}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, basket_id):
        rmc = message_collector()
        try:
            *auth_user, client_user_obj = get_user_obj_from_jwt_request(request)
             # check basket existence
            if not hasattr(client_user_obj, "basket"):
                rmc("User's basket not found")
                return Response({
                    "Error": rmc(),
                }, status=status.HTTP_404_NOT_FOUND)
            queryset = client_user_obj.basket
            
            basket_item = client_user_obj.basket.basket_item.get(id=basket_id)
            basket_item.delete()
            
            rmc("Item deleted successfully from basket.")
            
            return Response({
                "Message": rmc()
            }, status=status.HTTP_204_NO_CONTENT)
            
        except BasketItemModel.DoesNotExist as e:
            rmc(str(e))
            return Response({"Error": rmc()}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            rmc(str(e))
            return Response({"Error": rmc()}, status=status.HTTP_400_BAD_REQUEST)