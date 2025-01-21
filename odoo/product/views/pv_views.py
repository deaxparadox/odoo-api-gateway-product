from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.models import ProductVariantsModel
from product.serializers import pv_serializers

class ProductVariantsView(ListCreateAPIView):
    queryset = ProductVariantsModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = pv_serializers.PVSerializers
    
class ProductVariantDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    lookup_field = "id"
    queryset = ProductVariantsModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = pv_serializers.PVSerializersDetail
    
    def patch(self, request, *args, **kwargs):
        return Response({"Message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {"Message": "Variant Deleted Successfully"}
        return response