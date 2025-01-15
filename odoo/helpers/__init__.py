import hashlib
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

def create_variable_hash(data: str, /, *, length: int = 10):
    return hashlib.shake_256(data.encode()).hexdigest(length)

def get_user_id(token_str: str):
    access_token = AccessToken(token_str)
    user = User.objects.get(id=access_token['user_id'])
    return user.client_user.user_id