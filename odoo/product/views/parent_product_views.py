from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ProductCategoriesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get all product categories
        """
        return Response({"Message": "Get all product categories"})
    
    def post(self, request):
        """
        Create a new category
        """
        return Response({"Message": "Create a new category"})
    
    
class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get details of a specific category
        """
        return Response({"Message": "Get details of a specifc category"}, status=status.HTTP_200_OK)
    
    def put(self, request):
        """
        Update a category
        """
        return Response({"Message": "Update a category"}, status=status.HTTP_202_ACCEPTED)
    
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