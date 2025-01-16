from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import ClientUserModel

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class ClientUserDetailSerializer(serializers.ModelSerializer):
    auth_user = UserDetailSerializer()
    
    class Meta:
        model = ClientUserModel
        fields = ["user_id", "auth_user", "phone", "address"]

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["custom_field"] = "Custom value"

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data["user_id"] = self.user.client_user.user_id
        data["username"] = user.username
        # ... add other user information as needed

        return data
    
    
class UserDetailsObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["custom_field"] = "Custom value"

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data["user_id"] = self.user.client_user.user_id
        data["username"] = user.username
        data['email'] = user.email
        data['phone'] = user.phone
        # ... add other user information as needed

        return data
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()