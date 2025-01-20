from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from product import models
from product.serializers import product_serializer

class ProductCategoriesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get all product categories
        """    
        product_qs = models.ProductCategoryModel.objects.all()
        product_qs_serializer = product_serializer.ProductCategorySerializer(product_qs, many=True)
        return Response(product_qs_serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        """
        Create a new category
        """
        product_qs_serializer = product_serializer.ProductCategoryCreateSerializer(data=request.data)
        if product_qs_serializer.is_valid():
            pc_instance = product_qs_serializer.save()
            return_serializer = product_serializer.PCCreateReturnSerializer(pc_instance)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(product_qs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        """
        Get details of a specific category
        """
        product_qs = models.ProductCategoryModel.objects.get(id=id)
        product_qs_serializer = product_serializer.ProductCategorySerializer(product_qs)
        return Response(product_qs_serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id: int):
        """
        Update a category
        """
        update_serializer = product_serializer.ProductCategoryCreateSerializer(data=request.data)
        
        try:
            if update_serializer.is_valid():
                
                product_qs = models.ProductCategoryModel.objects.get(id=id)
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
        except Exception as e:
            return Response(
                {"Error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, request):
        """
        Delete a category
        """
        return Response({"Message": "Delete a category"}, status=status.HTTP_204_NO_CONTENT)
    
class ProductUnderCategoryVeiw(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get all products under a category
        """
        return Response({"Message": "Get all products under a category"}, status=status.HTTP_200_OK)