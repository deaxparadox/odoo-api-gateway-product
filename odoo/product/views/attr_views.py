from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.models import AttributesModel
from product.serializers import attr_serializers

class AttributesView(ListCreateAPIView):
    queryset = AttributesModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = attr_serializers.AttrsSerializers
    
class AttributesDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    lookup_field = "id"
    queryset = AttributesModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = attr_serializers.AttrsDetailSerializers
    
    def patch(self, request, *args, **kwargs):
        return Response({"Message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {"Message": "Variant Deleted Successfully"}
        return response