from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import ClientUserModel

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class ClientUserDetailSerializer(serializers.ModelSerializer):
    auth_user = UserDetailSerializer()
    
    class Meta:
        model = ClientUserModel
        fields = ["auth_user", "phone", "address"]
        

class ClientUserUpdateSerializer(serializers.ModelSerializer):
    auth_user = UserDetailSerializer()
    
    class Meta:
        model = ClientUserModel
        fields = ["user_id", "auth_user", "phone", "address"]
        
    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
    
    def update(self, instance, validated_data):
        auth_user_data = validated_data.pop('auth_user')
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        auth_user = instance.auth_user

        instance.username = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('address', instance.address)
        instance.save()

        auth_user.first_name = auth_user_data.get(
            'first_name',
            auth_user.first_name
        )
        auth_user.last_name = auth_user_data.get(
            'last_name',
            auth_user.last_name
        )
        # profile.save()
        auth_user.save()

        return instance

class AdminGetUsersSerializer(serializers.ModelSerializer):
    auth_user = UserDetailSerializer()
    class Meta:
        model = ClientUserModel
        fields = "__all__"

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

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()