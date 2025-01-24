from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import  vendor_serializer
from ..models import VendorsModel
from helpers.message import message_collector
from helpers.response import api_error_response, api_message_response

class VendorViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        rmc = message_collector()
        try:
            querset = VendorsModel.objects.all()
            serializer = vendor_serializer.VendorSerializer(querset)
            return api_message_response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            rmc(str(e))
            return api_error_response(status.HTTP_400_BAD_REQUEST, rmc())