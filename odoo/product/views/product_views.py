from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from product import models
from product.serializers import product_serializer
from helpers.permissions import OnlyVendor

class ProductCategoriesView(APIView):
    
    def get(self, request):
        """
        Get all product categories
        """
        product_scope = request.GET.get("active", None)
        product_qs = models.ProductCategoryModel.objects.all()
        if product_scope == 'true':
            product_qs = product_qs.filter(active=True)
        elif product_scope == 'false':
            product_qs = product_qs.filter(active=False)
        # print(product_qs)
        product_qs_serializer = product_serializer.ProductCategorySerializer(product_qs, many=True)
        return Response({"Message": product_qs_serializer.data}, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        """
        Create a new category
        
        - name: Required in while creating product, must be included in required, processed throught serializer
        - vendor_id: get vendor_id from request. If included in POST request data, then verify the vendor.
        - description: optional
        - parent_id: optional
        - child_ids: optional but empty list must be included
        """
        # product_qs_serializer = product_serializer.ProductCategoryCreateSerializer(data=request.data)
        # if product_qs_serializer.is_valid():
        #     pc_instance = product_qs_serializer.save()
        #     return_serializer = product_serializer.PCCreateReturnSerializer(pc_instance)
        #     return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(product_qs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.permission_classes = [IsAuthenticated, OnlyVendor]
        self.check_permissions(request)
        try:
            access_token = AccessToken(str(request.auth))
            client_vendor = User.objects.get(id=access_token['user_id']).client_vendor
            product_create_new = product_serializer.PCCreateSerializer(data=request.data)
            if product_create_new.is_valid():
                product_instance = product_create_new.create(product_create_new.validated_data)
                product_instance.vendor_id = client_vendor
                product_instance.save()
                return Response({"Message": "New category created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        """
        Get details of a specific category
        """
        try:
            product_qs = models.ProductCategoryModel.objects.get(id=id)
            if not product_qs.active:
                return Response({"Message": [
                    "Product doesnot exist"
                ]}, status=status.HTTP_400_BAD_REQUEST)    
            product_qs_serializer = product_serializer.ProductCategorySerializer(product_qs)
            return Response(product_qs_serializer.data, status=status.HTTP_200_OK)
        # Not product exist exception
        except models.ProductCategoryModel.DoesNotExist as e:
            return Response({"Message": [
                str(e)
            ]}, status=status.HTTP_400_BAD_REQUEST)    
        # Any other exception
        except Exception as e:
            return Response({"Message": [
                str(e)
            ]}, status=status.HTTP_400_BAD_REQUEST)    
    
    def put(self, request, id: int):
        """
        Update a category
        """
        
        update_serializer = product_serializer.ProductCategoryCreateSerializer(data=request.data)
        
        try:
            if update_serializer.is_valid():
                product_qs = models.ProductCategoryModel.objects.get(id=id)
                # Check product existence.
                if not product_qs.active:
                    return Response({"Message": ["Product doesnot exists"]}, status=status.HTTP_400_BAD_REQUEST)
                product_instance = update_serializer.update(product_qs, update_serializer.validated_data)
                return Response(
                    update_serializer.data, 
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    update_serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Doesnotexist exception
        except models.ProductCategoryModel.DoesNotExist as e:
            return Response({"Message": [
                str(e)
            ]}, status=status.HTTP_400_BAD_REQUEST)
        # Any other exception
        except Exception as e:
            return Response(
                {"Error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, request, id: int):
        """
        Delete a category
        """
        try:
            product = models.ProductCategoryModel.objects.get(id=id)
            product.delete()
            return Response({"Message": "Delete a category"}, status=status.HTTP_204_NO_CONTENT)
            
        # Doesnotexist exception
        except models.ProductCategoryModel.DoesNotExist as e:
            return Response({"Message": [
                str(e)
            ]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ProductsUnderCategoryVeiw(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, id: int) -> Response:
        """
        Get all products under a category
        """
        try:
            product_category = models.ProductCategoryModel.objects.get(id=id)
            product_qs = product_category.parent_product.all()
            # if product_scope == 'true':
            #     product_qs = product_qs.filter(active=True)
            # elif product_scope == 'false':
            #     product_qs = product_qs.filter(active=False)
            # print(product_qs)
            product_qs_serializer = product_serializer.ProductCategorySerializer(product_qs, many=True)
            return Response({"Message": product_qs_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"Error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )