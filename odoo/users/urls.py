from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from .views import user_view
from .views import vendor_view

app_name = "users"

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', user_view.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('auth/logout/', user_view.LogoutView.as_view(), name='token_blacklist'),
    
    
    
    # POST: Create users
    path("users/", user_view.UserCreateView.as_view(), name="auth_create_user"),
    
    # GET: Get user details
    # PUT: Update user details
    # DELETE: Delete users
    path("users/<str:user_id>/", user_view.UserSpecificDetailView.as_view(), name="get_user_detail"),
    # path("users/<str:id>/", views.DeleteUserView.as_view(), name="delete_user")
    
    
    # Vendor endpoints
    # GET: get all Vendors
    # POST: Create users
    path("vendors/", vendor_view.VendorViews.as_view(), name="create_vendor"),
    
    # GET: Get user details
    # PUT: Update user details
    # DELETE: Delete users
    path("vendors/<str:vendor_id>/", vendor_view.VendorDetailsView.as_view(), name="vendor_detail"),
    
    
    
]
