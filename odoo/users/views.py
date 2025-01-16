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
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import (
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    UserDetailsObtainPairSerializer,
    ClientUserDetailSerializer,
    LogoutSerializer,
    AdminGetUsersSerializer
)
from users.models import ClientUserModel
import helpers



# Create a new user. 
class UserCreateView(APIView):
    
    """
    This class provide two functionality.
    
    1. POST: Create a user, using POST request.
    2. GET: `Admin` Get the list of all user.
    """
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        http_authorization = request.META.get("HTTP_AUTHORIZATION")
        if not http_authorization:
            return Response({"error": "User not authentication"}, status=status.HTTP_401_UNAUTHORIZED)
        token = http_authorization.split(" ")[1]
        access_token = AccessToken(token=token)
        user = User.objects.get(id=access_token['user_id'])
        if user.is_superuser:
            users = [u for u in ClientUserModel.objects.all() if not u.auth_user.is_superuser]
            users_serializers = AdminGetUsersSerializer(users, many=True)
            return Response(users_serializers.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Only admins allowed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
            
            
    def post(self, request, format=None):
        seriailzer = UserSerializer(data=request.data)
        # If for some reason unable to create a user
        # return it
        current_user = None
        if seriailzer.is_valid():
            # Create a user.
            # User must return a request with `email`.
            
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
        return Response(seriailzer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Get user specific details
# class UserSpecificDetailView(TokenObtainPairView):
#     serializer_class = UserDetailsObtainPairSerializer
class UserSpecificDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id: str):
        client_user = ClientUserModel.objects.get(user_id=id)
        client_serializer = ClientUserDetailSerializer(client_user)
        print(client_serializer.data)
        return Response(client_serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        # print(request.auth)
        http_authorization = request.auth
        # print(http_authorization, type(http_authorization))
        
        refresh_serializer = LogoutSerializer(data=request.data)
        if refresh_serializer.is_valid():
            # disable the user
            try:
                access_token = AccessToken(str(http_authorization))
                user = User.objects.get(id=access_token['user_id'])
                user.is_active = False
                user.save()
            except Exception as e:
                return Response({"error": "Access token " + str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            # Invalid the refresh token
            try:
                refresh_token = RefreshToken(refresh_serializer.validated_data.get("refresh"))
                refresh_token.blacklist()
            except Exception as e:
                return Response({"error": "Refresh token" + str(e)}, status=status.HTTP_401_UNAUTHORIZED)
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
                Response({
                        "message": "Token blacklisted"
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": "Require `refresh` token to invalid."}, status=status.HTTP_400_BAD_REQUEST)
    
    
# Delete user
# class DeleteUserView(APIView):