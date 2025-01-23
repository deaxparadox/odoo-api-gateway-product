from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import BasketSerializer
from .models import BasketModel
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
            return Response({"Message": serializer.data}, status=status.HTTP_200_OK)
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