from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from product.models import ProductVariantsModel
from product.serializers import pv_serializers
from notifications.models import NotificationModel
from helpers.permissions import OnlyVendor

class ProductVariantsView(ListCreateAPIView):
    lookup_field = 'pk'
    queryset = ProductVariantsModel.objects.all()
    
    

    
    def get(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticatedOrReadOnly]
        self.check_permissions(request)
        self.serializer_class = pv_serializers.PVSerializers
        response = super().get(request, *args, **kwargs)        
        return response
    
    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, OnlyVendor]
        self.check_permissions(request)
        self.serializer_class = pv_serializers.PVCreateSerializers
        response = super().post(request, *args, **kwargs)
        
        notify = NotificationModel.objects.create(
            title="Created: Product variant",
            body="Product variant with parent_id %s and id %s created successfully" % (
                response.data['product_template_id'], response.data['id']
            )
        )
        notify.vendor_user.add(request.user.client_vendor)

        response.data = {"Message": response.data}
        return response
    
class ProductVariantDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    lookup_field = "id"
    queryset = ProductVariantsModel.objects.all()
    permission_classes = [IsAuthenticated, OnlyVendor]
    serializer_class = pv_serializers.PVSerializersDetail
    
        
    def get_object(self):
        self.instance =  super().get_object()
        return self.instance
    
    def put(self, request, *args, **kwargs):
        # instance = self.get_object()
        response = super().put(request, *args, **kwargs)
        
        notify = NotificationModel.objects.create(
            title="Updated: Product variant",
            body="Product variant with parent_id %s and id %s updated successfully" % (
                response.data['product_template_id'], response.data['id']
            )
        )
        notify.vendor_user.add(request.user.client_vendor)
        response.data = {"Message": response.data}
        return response
    
    def patch(self, request, *args, **kwargs):
        return Response({"Message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().delete(request, *args, **kwargs)
        
        notify = NotificationModel.objects.create(
            title="Deleted: Product variant",
            body="Product variant with %s deleted successfully" % instance.id
        )
        notify.vendor_user.add(request.user.client_vendor)
        
        response.data = {"Message": "Variant Deleted Successfully"}
        return response