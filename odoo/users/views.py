from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings
from users.serializers import UserSerializer
from users.models import ClientUserModel
import helpers



# Create a new user. 
class UserCreateView(APIView):
    def post(self, request, format=None):
        seriailzer = UserSerializer(data=request.data)
        if seriailzer.is_valid():
            try:
                auth_user = User.objects.create_user(
                    username=seriailzer.validated_data.get("username"),
                    password=seriailzer.validated_data.get("password")
                )
                client_user = ClientUserModel.objects.create(
                    user_id = helpers.create_variable_hash(auth_user.email),
                    auth_user=auth_user
                )
            except Exception as e:
                # print(dict(seriailzer.data))
                return Response(
                    {
                        "error": str(e)
                    }, 
                    status=status.HTTP_409_CONFLICT
                )
            return Response({
                "message": "User create successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(seriailzer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login
class UserLoginBase(TokenViewBase):

    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        # Manipulating data response data
        access_token = serializer.validated_data['access']
        new_data = {
            "access": access_token,
            "refresh": serializer.validated_data['refresh'],
            "user_id": helpers.get_user_id(access_token)
        }
        # print(self.get_user_id(access_token))
        # return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(new_data, status=status.HTTP_200_OK)


class UserLoginPairView(UserLoginBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER


# Get user specific details
class UserSpecificDetailView(APIView):
    def get(self, request, **kwargs):
        print(request.META.get("HTTP_UT"))
        return Response({}, status=status.HTTP_200_OK)