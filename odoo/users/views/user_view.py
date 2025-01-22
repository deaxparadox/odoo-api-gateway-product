import logging
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import (
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    UserDetailsObtainPairSerializer,
    ClientUserDetailSerializer,
    ClientUserUpdateSerializer,
    LogoutSerializer,
    AdminGetUsersSerializer
)
from users.models import ClientUserModel
import helpers


logger = logging.getLogger(__name__)


class AdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        all_active_user = [u for u in ClientUserModel.objects.all() if u.auth_user.is_active == True]
        serializer = AdminGetUsersSerializer(all_active_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Create a new user. 
class UserCreateView(APIView):
    """
    This class provide two functionality.
    
    1. POST: Create a user, using POST request.
    2. GET: `Admin` Get the list of all user.
    """
    # permission_classes = [IsAuthenticated]
    
    def get(self, request: Request):
        """
        Admin User return the list of all users.
        """
        # http_authorization = request.META.get("HTTP_AUTHORIZATION")
        http_authorization = request.auth
        if not http_authorization:
            return Response({"error": "User not authentication"}, status=status.HTTP_401_UNAUTHORIZED)
        # token = http_authorization.split(" ")[1]
        try:
            # print(http_authorization)
            access_token = AccessToken(token=str(http_authorization))
            user = User.objects.get(id=access_token['user_id'])
            if user.is_superuser:
                users = [u for u in ClientUserModel.objects.all() if not u.auth_user.is_superuser]
                users_serializers = AdminGetUsersSerializer(users, many=True)
                return Response(users_serializers.data, status=status.HTTP_200_OK)
            return Response(
                {"message": "Only admins allowed"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except TokenError as e:
            return Response({"Error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    def post(self, request, format=None):
        logger.warning("Creating a new user.")
        """
        Create a user.
        """
        seriailzer = UserSerializer(data=request.data)
        # If for some reason unable to create a user
        # return it
        current_user = None
        if seriailzer.is_valid():
            # Create a user.
            
            # User must request with `email`.
            
            # Search for username and email
            if (
                len(User.objects.filter(username=seriailzer.validated_data.get("username"))) > 0 or 
                len(User.objects.filter(username=seriailzer.validated_data.get("email"))) > 0 
            ):
                return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create user
            try:
                current_user = auth_user = User.objects.create_user(
                    username=seriailzer.validated_data.get("username"),
                    email=seriailzer.validated_data.get("email"),
                    password=seriailzer.validated_data.get("password")
                )
            except Exception as e:
                return Response(
                    {
                        "error": "user " + str(e)
                    }, 
                    status=status.HTTP_409_CONFLICT
                )
            # Create a client user.
            try:
                client_user = ClientUserModel.objects.create(
                    user_id = helpers.create_variable_hash(auth_user.email),
                    auth_user=auth_user
                )
            except Exception as e:
                # if error occur while creating client user,
                # remove the auth_user
                current_user.delete()
                return Response(
                    {
                        "error": "client user " + str(e),
                    },
                    status=status.HTTP_204_NO_CONTENT
                )
            # Return a user created response
            return Response({
                "message": "User create successfully"
            }, status=status.HTTP_201_CREATED)
        # Invalid details
        return Response(seriailzer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    User login.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        # print(request.user)
        return super().post(request, *args, **kwargs)


# Get user specific details
# class UserSpecificDetailView(TokenObtainPairView):
#     serializer_class = UserDetailsObtainPairSerializer
class UserSpecificDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id: str):
        """
        Get user details.
        """
        
        client_user = ClientUserModel.objects.get(user_id=user_id)
        client_serializer = ClientUserDetailSerializer(client_user)
        print(client_serializer.data)
        return Response(client_serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, user_id: str):
        """
        Update user details.
        """
        http_authorization = request.auth
        client_user_instance = ClientUserModel.objects.get(user_id=user_id)
        client_update_serializer = ClientUserUpdateSerializer(data=request.data, instance=client_user_instance, partial=True)
        
        
        try:
            access_token = AccessToken(str(http_authorization))
            # print(client_user_instance.auth_user.id, access_token['user_id'])
            if client_user_instance.auth_user.id != access_token['user_id']: 
                return Response({"error": "Invalid users details"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        
        
        if client_update_serializer.is_valid():
            print(client_update_serializer.validated_data)
            # client_update_serializer.update()
            client_update_serializer.save()
            return Response(client_update_serializer.validated_data, status=status.HTTP_202_ACCEPTED)
        return Response(client_update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, user_id: str):
        """
        Delete user accounts.
        """
        # print(request.auth)
        http_authorization = request.auth
        # print(http_authorization, type(http_authorization))
        client_user_instance = ClientUserModel.objects.get(user_id=user_id)
        try:
            access_token = AccessToken(str(http_authorization))
            # print(client_user_instance.auth_user.id, access_token['user_id'])
            if client_user_instance.auth_user.id != access_token['user_id']: 
                return Response({"error": "Invalid users details"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
        
        refresh_serializer = LogoutSerializer(data=request.data)
        if refresh_serializer.is_valid():
            # disable the user
            try:
                user = User.objects.get(id=access_token['user_id'])
                user.is_active = False
                user.save()
            except Exception as e:
                return Response({"error": "Access token " + str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            # Invalid the refresh token,
            # user must be disabled for refresh token to be blacklisted
            try:
                refresh_token = RefreshToken(refresh_serializer.validated_data.get("refresh"))
                refresh_token.blacklist()
            except Exception as e:
                return Response({"error": "Refresh token " + str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"message": "User successfully deleted"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # authorization = request.META.get("HTTP_AUTHORIZATION")
        # if not authorization:
        #     return Response({
        #         "error": "Unauthentication user."
        #     }, status=status.HTTP_401_UNAUTHORIZED)
        logout_serializer = LogoutSerializer(data=request.data)
        if logout_serializer.is_valid():
            # print(logout_serializer.data, authorization)
            try:
                refresh_token = RefreshToken(logout_serializer.data.get("refresh"))
                refresh_token.blacklist()
                return Response({
                        "Message": "Token blacklisted"
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": "Require `refresh` token."}, status=status.HTTP_400_BAD_REQUEST)
    
    
# Delete user
# class DeleteUserView(APIView):