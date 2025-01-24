from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from ..serializers import  vendor_serializer
from ..models import VendorsModel
from ..serializers.user_serializers import AdminGetUsersSerializer, UserSerializer, ClientUserUpdateSerializer
import helpers
from helpers.message import message_collector
from helpers.response import api_error_response, api_message_response
from basket.views import get_user_obj_from_jwt_request

class VendorViews(APIView):
    def get(self, request):
        "Get all vendors"
        rmc = message_collector()
        try:
            *auth_user, client_user = get_user_obj_from_jwt_request(request)
            querset = VendorsModel.objects.all()
            serializer = vendor_serializer.VendorSerializer(querset, many=True)
            return api_message_response(serializer.data, status.HTTP_200_OK)
        except TokenError as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        """
        Create a vendor.
        """
        rmc = message_collector()
    
        print(f"Checking request: {request.data}")
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # Create a user.
            
                # User must request with `email`.
                
                # Search for username and email
                if (
                    len(User.objects.filter(username=serializer.validated_data.get("username"))) > 0 or 
                    len(User.objects.filter(username=serializer.validated_data.get("email"))) > 0 
                ):
                    rmc("User already exists")
                    return api_error_response(rmc, status=status.HTTP_400_BAD_REQUEST)
                
                # Create user
                try:
                    current_user = auth_user = User.objects.create_user(
                        username=serializer.validated_data.get("username"),
                        email=serializer.validated_data.get("email"),
                        password=serializer.validated_data.get("password")
                    )
                except Exception as e:
                    rmc("vendor client " + str(e))
                    return api_error_response(
                        rmc,
                        status=status.HTTP_409_CONFLICT
                    )
                # Create a client user.
                try:
                    user_id = helpers.create_variable_hash(auth_user.email)
                    print(user_id, len(user_id))
                    client_user = VendorsModel.objects.create(
                        user_id = user_id,
                        auth_user=auth_user
                    )
                except Exception as e:
                    # if error occur while creating client user,
                    # remove the auth_user
                    current_user.delete()
                    rmc("client user " + str(e))
                    return api_error_response(
                        rmc,
                        status=status.HTTP_204_NO_CONTENT
                    )
                
                rmc("Vendor created successfully")
                return api_message_response(rmc, status.HTTP_201_CREATED)
            rmc(serializer.errors)
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        
class VendorDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_id):
        rmc = message_collector()
        try:
            vendor = VendorsModel.objects.get(user_id=vendor_id)
            serializer = vendor_serializer.VendorClientDetailSerializer(vendor)
            return api_message_response(serializer.data, status.HTTP_200_OK)
        except VendorsModel.DoesNotExist as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, vendor_id):
        """
        Update vendors detils
        
        - Only vendor should be able to update its details.
        """
        rmc = message_collector()
        try:
            vendor = VendorsModel.objects.get(user_id=vendor_id)
            token = str(request.auth)
            access_token = AccessToken(token)
            if vendor.user_id != access_token['user_id']:
                rmc("Invalid access token and user_id")
                return api_error_response(rmc, status.HTTP_401_UNAUTHORIZED)
            serializer = ClientUserUpdateSerializer(data=request.data)
            if serializer.is_valid():
                vendor_update = serializer.update(vendor, serializer.validated_data)
                serializer_update = vendor_serializer.VendorSerializer(vendor_update)
                # rmc("Successfully updated user details")
                return api_message_response(serializer_update.data, status.HTTP_202_ACCEPTED)
            return api_error_response(serializer.data, status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        except VendorsModel.DoesNotExist as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            rmc(str(e))
            return api_error_response(rmc, status.HTTP_400_BAD_REQUEST)
        
    # def dlete