from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import NotificationModel
from product.models import AttributesModel
from product.serializers import attr_serializers
from helpers.permissions import OnlyVendor

class AttributesView(ListCreateAPIView):
    queryset = AttributesModel.objects.all()
    permission_classes = [IsAuthenticated, OnlyVendor]
    serializer_class = attr_serializers.AttrsSerializers
    
    def post(self, request, *args, **kwargs):
        serializer = attr_serializers.AttrsCreateSerializers(data=request.data)
        try:
            if serializer.is_valid():
                instance = serializer.save()
                # Create a notifications about newly added attribute
                notify = NotificationModel.objects.create(
                    title="Attribute created %s" % instance.name,
                    body="Attribute with name %s and id %s created successfully" % (instance.name, instance.id)
                )
                notify.vendor_user.add(request.user.client_vendor)
                notify.save()
                ret_serializer = attr_serializers.AttrsSerializers(instance)
                return Response({"Message": ret_serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class AttributesDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    lookup_field = "id"
    queryset = AttributesModel.objects.all()
    permission_classes = [IsAuthenticated, OnlyVendor]
    serializer_class = attr_serializers.AttrsDetailSerializers
    
    def get_object(self):
        self.instance =  super().get_object()
        return self.instance
    
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        notify = NotificationModel(
            title="Update: %s" % self.instance.name,
            body="Attribute name %s and id %s updated successfully" % (self.instance.name, self.instance.id)
        )
        notify.save()
        notify.vendor_user.add(request.user.client_vendor)
        return response
    
    def patch(self, request, *args, **kwargs):
        return Response({"Message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {"Message": "Variant Deleted Successfully"}
        return response