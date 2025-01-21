from django.urls import path
from product.views import product_views
from product.views import pp_views, pv_views

app_name = "product"

urlpatterns = [
    
    # Product Category
    # 
    # GET: Get all product categories
    # POST: Create a new product
    path("categories/", product_views.ProductCategoriesView.as_view(), name="get_product_categories"),
    # GET: Get detail of specific category (using id)
    # PUT: Update category details
    # DELETE: Delete a category
    path("categories/<int:id>/", product_views.ProductView.as_view(), name="get_product_categories"),
    
    
    # Parent product Category
    # 
    # GET: all parent products
    # POST: Create a new product
    path("products/", pp_views.ParentProductView.as_view(), name="parent_product_view"),
    # 
    # GET: Get details of a specific product
    # PUT: Update product details
    # DELETE: Delete a product   
    path("products/<int:id>/", pp_views.ParentProductDetailView.as_view(), name="parent_product_detail"),
    
    
    # Parent variant Category
    # 
    # GET: all products variant
    # POST: Create a new variant
    path("variants/", pv_views.ProductVariantsView.as_view(), name="product_variant_view"),
    # 
    # GET: Get details of a specific variant
    # PUT: Update variant details
    # DELETE: Delete a variant   
    path("variants/<int:id>/", pv_views.ProductVariantDetailView.as_view(), name="product_variant_detail")
]
