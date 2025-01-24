from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import ClientUserModel, AddressModel


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        exclude = ['vendor_id']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class ClientUserDetailSerializer(serializers.ModelSerializer):
    auth_user = UserDetailSerializer()
    address = AddressSerializer(many=True,read_only=True)
    
    class Meta:
        model = ClientUserModel
        fields = ["user_id", "auth_user", "phone", "address"]
        


class AddressUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    address1 = serializers.CharField()
    address2 = serializers.CharField(required=False)
    state = serializers.CharField()
    country = serializers.CharField()
    user_id = serializers.CharField()
    
class ClientUserUpdateSerializer(serializers.ModelSerializer):
    auth_user = UserDetailSerializer()
    address = AddressUpdateSerializer(many=True)
    
    class Meta:
        model = ClientUserModel
        fields = ["user_id", "auth_user", "phone", "address"]
        
    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
    
    def update(self, instance, validated_data):
        auth_user_data = validated_data.pop('auth_user')
        address = validated_data.pop("address")
        # Unless the application properly enforces that this field is
        # always set, the following could raise a `DoesNotExist`, which
        # would need to be handled.
        auth_user = instance.auth_user
        
        for add in address:
            add.pop('user_id')
            add_inst = AddressModel.objects.get(id=add.pop('id'))
            add_inst.address1 = add.get("address1", add_inst.address1)
            add_inst.address2 = add.get("address2", None)
            add_inst.state = add.get("state", add_inst.state)
            add_inst.country = add.get("country", add_inst.country)
            add_inst.save()
            
        instance.phone = validated_data.get('phone', instance.phone)
        # instance.address = validated_data.get('address', instance.address)
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
        if hasattr(user, "client_user"):
            data["user_id"] = self.user.client_user.user_id
            data["username"] = user.username
        if hasattr(user, 'client_vendor'):
            data['vendor_id'] = self.user.client_vendor.user_id
            data['username'] = user.username
        # ... add other user information as needed

        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()