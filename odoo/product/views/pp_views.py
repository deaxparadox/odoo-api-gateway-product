# Parent product view 


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from product.serializers import pp_serializers
from product.models import ParentProductModel
from notifications.models import NotificationModel
from helpers.permissions import OnlyVendor

class ParentProductView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get all parent products.
        
        - Permission: is set to Authentication and ReadOnly for unauthenticated user.
        """
        self.permission_classes = [IsAuthenticatedOrReadOnly]
        self.check_permissions(request)
        qs = ParentProductModel.objects.all()
        qs_serializer = pp_serializers.PPSerializers(qs, many=True)
        return Response({"Products": qs_serializer.data}, status=status.HTTP_200_OK)
        # return Response({"Message": "Get all product categories"})
    
    def post(self, request):
        """
        Create a new product.
        
        Required data in request:
        1. name
        2. category_ids: If not category ids are given, then an empty list must be passed.
        
        Optional data in request:
        1. description
        2. Image URL
        3. List price
        """
        self.permission_classes = [IsAuthenticated, OnlyVendor]
        self.check_permissions(request)
        try:
            # print(request.data)
            pps = pp_serializers.PPCreateSerializer(data=request.data)
            if pps.is_valid():
                instance = pps.save()
                ret_serializer = pp_serializers.PPSerializers(instance)
                
                notify = NotificationModel.objects.create(
                    title="Created: Product",
                    body="Product name %s with ID %s created successfully" % (instance.name, instance.id)
                )
                notify.vendor_user.add(request.user.client_vendor)
                
                return Response(ret_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(pps.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        
class ParentProductDetailView(APIView):
    
    def get(self, request, id: int):
        """
        Get details of a specific product.
        """
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        try:
            qs = ParentProductModel.objects.filter(id=id)
            if len(qs) == 0: return Response({"Message": ['Product doesnot exists']}, status=status.HTTP_400_BAD_REQUEST)
            product = qs[0]
            serializer = pp_serializers.PPSerializers(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"Message": "Get details of a specifc category"}, status=status.HTTP_200_OK)
    
    def put(self, request, id: int):
        """
        Update product details.
        """
        self.permission_classes = [IsAuthenticated, OnlyVendor]
        self.check_permissions(request)
        try:
            qs = ParentProductModel.objects.get(id=id)
            serializer = pp_serializers.PPCreateSerializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.update(qs, serializer.validated_data)
                
                notify = NotificationModel.objects.create(
                    title="Updated: Product",
                    body="Product name %s with ID %s updated successfully" % (instance.name, instance.id)
                )
                notify.vendor_user.add(request.user.client_vendor)
                
                return Response({"Message": serializer.data}, status=status.HTTP_202_ACCEPTED)
            return Response({"Error": serializer.errors}, status=status.HTTP_202_ACCEPTED)
        except ParentProductModel.DoesNotExist as e:
            return Response({"Error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id: int):
        """
        Delete a product.
        """
        self.permission_classes = [IsAuthenticated, OnlyVendor]
        self.check_permissions(request)
        try:
            instance = ParentProductModel.objects.get(id=id)
            
            notify = NotificationModel.objects.create(
                title="Updated: Product",
                body="Product name %s with ID %s updated successfully" % (instance.name, instance.id)
            )
            notify.vendor_user.add(request.user.client_vendor)
            
            instance.delete()
                
                
            return Response({"Message": "Delete a category"}, status=status.HTTP_204_NO_CONTENT)
        except ParentProductModel.DoesNotExist as e:
            return Response({"Error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)
        
class ProductSyncVeiw(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Get all products under a category
        """
        return Response({"Message": "Get all products under a category"}, status=status.HTTP_200_OK)