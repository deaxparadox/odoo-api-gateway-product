from django.urls import path
from product.views import pp_views, pv_views, attr_views, attr_value_views, pc_view

app_name = "product"

urlpatterns = [
    
    # Product Category
    # 
    # GET: Get all product categories
    # POST: Create a new product
    path("categories/", pc_view.ProductCategoriesView.as_view(), name="product_categories_view"),
    # GET: Get detail of specific category (using id)
    # PUT: Update category details
    # DELETE: Delete a category
    path("categories/<int:id>/", pc_view.ProductView.as_view(), name="product_categories_detail_view"),
    # GET: Product under a category
    path("categories/<int:id>/products/", pc_view.ProductsUnderCategoryVeiw.as_view(), name="product_categories_detail_view"),
    
    
    # Parent product Category
    # 
    # GET: all parent products
    # POST: Create a new product
    path("products/", pp_views.ParentProductView.as_view(), name="parent_product_view"),
    # 
    # GET: Get details of a specific product
    # PUT: Update product details
    # DELETE: Delete a product   
    path("products/<int:id>/", pp_views.ParentProductDetailView.as_view(), name="parent_product_detail_view"),
    
    
    # Parent variant Category
    # 
    # GET: all products variant
    # POST: Create a new variant
    path("variants/", pv_views.ProductVariantsView.as_view(), name="product_variant_view"),
    # 
    # GET: Get details of a specific variant
    # PUT: Update variant details
    # DELETE: Delete a variant   
    path("variants/<int:id>/", pv_views.ProductVariantDetailView.as_view(), name="product_variant_detail_view"),
    
    
    # Attributes Category
    # 
    # GET: all products variant
    # POST: Create a new variant
    path("attributes/", attr_views.AttributesView.as_view(), name="attributes_view"),
    # 
    # GET: Get details of a specific variant
    # PUT: Update variant details
    # DELETE: Delete a variant   
    path("attributes/<int:id>/", attr_views.AttributesDetailView.as_view(), name="attributes_detail_view"),
    
    
    # Attributes Category
    # 
    # GET: all value based on attribute ID
    # POST: Create a new value based on attribute ID
    path("attributes/<int:attr_id>/values/", attr_value_views.AttributeValueView.as_view(), name="av_view"),
    # 
    # GET: Get details of a specific value based on ID
    # PUT: Update value details based on ID
    # DELETE: Delete a value based on ID
    path("attributes/<int:attr_id>/values/<int:value_id>/", attr_value_views.AVUpdateDeleteView.as_view(), name="av_create_update_view")
]
