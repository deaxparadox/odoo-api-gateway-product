from django.urls import path
from product.views import product_views

app_name = "product"

urlpatterns = [
    # GET: Get all product categories
    path("categories/", product_views.ProductCategoriesView.as_view(), name="get_product_categories"),
    
    # GET: Get detail of specific category (using id)
    path("categories/<int:id>/", product_views.ProductView.as_view(), name="get_product_categories")
]
