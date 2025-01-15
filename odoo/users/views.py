from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.models import TokenUser
from users.serializers import UserSerializer

class UserCreateView(APIView):
    def post(self, request, format=None):
        seriailzer = UserSerializer(data=request.data)
        if seriailzer.is_valid():
            try:
                user = User.objects.create_user(
                    username=seriailzer.validated_data.get("username"),
                    password=seriailzer.validated_data.get("password")
                )
            except Exception as e:
                # print(dict(seriailzer.data))
                return Response(
                    {
                        "error": str(e),
                        **seriailzer.data
                    }, 
                    status=status.HTTP_409_CONFLICT
                )
            return Response({
                "message": "User create successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(seriailzer.errors, status=status.HTTP_400_BAD_REQUEST)