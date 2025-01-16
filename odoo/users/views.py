from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings
from users.serializers import (
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    UserDetailsObtainPairSerializer,
    ClientUserDetailSerializer,
    LogoutSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken    
from users.models import ClientUserModel
import helpers



# Create a new user. 
class UserCreateView(APIView):
    def post(self, request, format=None):
        seriailzer = UserSerializer(data=request.data)
        if seriailzer.is_valid():
            # Create a user.
            # User must return a request with `email`.
            try:
                auth_user = User.objects.create_user(
                    username=seriailzer.validated_data.get("username"),
                    email=seriailzer.validated_data.get("email"),
                    password=seriailzer.validated_data.get("password")
                )
            except Exception as e:
                return Response(
                    {
                        "error": str(e)
                    }, 
                    status=status.HTTP_409_CONFLICT
                )
            # Create a client user.
            print(auth_user.username, auth_user.email)
            try:
                client_user = ClientUserModel.objects.create(
                    user_id = helpers.create_variable_hash(auth_user.email),
                    auth_user=auth_user
                )
            except Exception as e:
                return Response(
                    {
                        "error": str(e),
                    },
                    status=status.HTTP_204_NO_CONTENT
                )
            # Return a user created response
            return Response({
                "message": "User create successfully"
            }, status=status.HTTP_201_CREATED)
        # Invalid details
        return Response(seriailzer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login
# class UserLoginBase(TokenViewBase):
#     def post(self, request: Request, *args, **kwargs) -> Response:
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])
        
#         # Manipulating data response data
#         access_token = serializer.validated_data['access']
#         new_data = {
#             "access": access_token,
#             "refresh": serializer.validated_data['refresh'],
#             "user_id": helpers.get_user_id(access_token)
#         }
#         # print(self.get_user_id(access_token))
#         # return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(new_data, status=status.HTTP_200_OK)
# 
# 
# class UserLoginPairView(UserLoginBase):
#     """
#     Takes a set of user credentials and returns an access and refresh JSON web
#     token pair to prove the authentication of those credentials.
#     """
#     _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER
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
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        authorization = request.META.get("HTTP_AUTHORIZATION")
        if not authorization:
            return Response({
                "error": "Unauthentication user."
            }, status=status.HTTP_401_UNAUTHORIZED)
        logout_serializer = LogoutSerializer(data=request.data)
        if logout_serializer.is_valid():
            # print(logout_serializer.data, authorization)
            try:
                refresh_token = RefreshToken()
                refresh_token.blacklist()
            except Exception as e:
                Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({}, status=status.HTTP_202_ACCEPTED)
        return Response({"Error": "Require `refresh` token to invalid."}, status=status.HTTP_400_BAD_REQUEST)