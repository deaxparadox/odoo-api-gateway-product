from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import BasketSerializer
from .models import BasketModel
from helpers.message import message_collector

class BasketView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        rmc = message_collector()
        token = str(request.auth)
        try:
            auth_user_id = AccessToken(token)['user_id']
            auth_user_obj = User.objects.get(id=auth_user_id)
            client_user_obj = auth_user_obj.client_user
            # print(hasattr(client_user_obj, 'basket'))
            if not hasattr(client_user_obj, "basket"):
                rmc("User's basket not found")
                return Response({
                    "Error": rmc(),
                }, status=status.HTTP_404_NOT_FOUND)
            queryset = client_user_obj.basket.all()
            serializer = BasketSerializer(queryset, many=True)
            return Response({"Message": serializer.data}, status=status.HTTP_200_OK)
        except TokenError as e:
            rmc(str(e))
            return Response(
                {"Error": rmc()},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            rmc(str(e))
            return Response(
                {"Error": rmc()},
                status=status.HTTP_400_BAD_REQUEST
            )