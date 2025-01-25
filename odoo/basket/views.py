from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import (
    BasketSerializer, 
    BasketVariantSerializer, 
    BasketQuantitySerializer,
    BasketItemAddSerializers
)
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

class Basket:
    def build_basket(self, user_basket: BasketModel):
        serializer = BasketSerializer(user_basket)
        data = {**serializer.data}
        # Total value of basket
        basket_items = user_basket.basket_item.all()
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
        return data

class BasketView(APIView, Basket):
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
            data = self.build_basket(client_user_obj.basket)
            # queryset = client_user_obj.basket
            # serializer = BasketSerializer(queryset)
            # data = {**serializer.data}
            # # Total value of basket
            # basket_items = queryset.basket_item.all()
            # data['total_price'] = sum(x.total_price() for x in basket_items)
            # data['products'] = []
            # for item in basket_items:
            #     pv_serializsers = BasketVariantSerializer(item.product_id)
            #     q = {
            #         "quantity": item.quantity,
            #         "basket_item_id": item.id
            #     }
            #     q.update({**pv_serializsers.data})
            #     # change variant referene from `id` to `product_variant_id`
            #     product_variant_id = q.pop("id")
            #     q.update({"product_variant_id": product_variant_id})
            #     # q.pop('price_extra')
            #     # q.pop("barcode")
            #     # q.pop("sku")
            #     data["products"].append(q)
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
            
class BasketItem(APIView, Basket):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # add item to the basket
        rmc = message_collector()
        
        try:
            *auth_user, client_user_obj = get_user_obj_from_jwt_request(request)
            pv_serializers = BasketItemAddSerializers(data=request.data)
            if pv_serializers.is_valid():
                # check for basket existence
                if not hasattr(client_user_obj, "basket"):
                    rmc("User's basket not found")
                    return Response({
                        "Error": rmc(),
                    }, status=status.HTTP_404_NOT_FOUND)
                basket = client_user_obj.basket
                # get product_template_id from request data
                product_template_id = pv_serializers.validated_data.get("product_template_id", None)
                quantity = pv_serializers.validated_data.get("quantity", None)
                if not product_template_id:
                    rmc("Product not found in request to add")
                    return Response(
                        {"Error": rmc()},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if not quantity:
                    rmc("Invalid quantity")
                    return Response(
                        {"Error": rmc()},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                print(f"\nProduct template id: {product_template_id}\n")
                product = ProductVariantsModel.objects.get(id=product_template_id)
                basket_item = BasketItemModel.objects.create(
                    basket_id=client_user_obj.basket, 
                    product_id=product, 
                    quantity=quantity
                )
                data = self.build_basket(client_user_obj.basket)
                return Response(
                    {"Message": data},
                    status=status.HTTP_202_ACCEPTED
                )
            # rmc(pv_serializers.data)
            return Response({"Error": pv_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            rmc(str(e))
            return Response({"Error": rmc()}, status=status.HTTP_400_BAD_REQUEST)
    
class BasketModifyView(APIView, Basket):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, basket_id):
        """
        Update the quantity of basket item.
        - Will get User ID from request
        - Will Basket ID from User instance
        - WIll get BasketItem ID from url path
        """
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
                basket = client_user_obj.basket
                
                # update basket
                basket_item = basket.basket_item.get(id=basket_id)
                basket_item.quantity = quantity_serializer.validated_data['quantity']
                basket_item.save()
                
                # fetch data for display
                # serializer = BasketSerializer(basket)
                # data = {**serializer.data}
                # # Total value of basket
                # basket_items = basket.basket_item.all()
                # data['total_price'] = sum(x.total_price() for x in basket_items)
                # data['products'] = []
                # for item in basket_items:
                #     pv_serializsers = BasketVariantSerializer(item.product_id)
                #     q = {
                #         "quantity": item.quantity,
                #         "basket_item_id": item.id
                #     }
                #     q.update({**pv_serializsers.data})
                #     # change variant referene from `id` to `product_variant_id`
                #     product_variant_id = q.pop("id")
                #     q.update({"product_variant_id": product_variant_id})
                #     data["products"].append(q)
                data = self.build_basket(basket)
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
        
        
class BasketClear(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        rmc = message_collector()
        try:
            *auth_user, client_user_obj = get_user_obj_from_jwt_request(request)
            if not hasattr(client_user_obj, "basket"):
                rmc("User's basket not found")
                return Response({
                    "Error": rmc(),
                }, status=status.HTTP_404_NOT_FOUND)
            basket = client_user_obj.basket
            for item in basket.basket_item.all():
                item.delete()
            return Response({"Message": "Basket cleared"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            rmc(str(e))
            return Response({"Error": rmc()}, status=status.HTTP_400_BAD_REQUEST)