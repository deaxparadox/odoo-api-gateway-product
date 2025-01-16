from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from users import views

app_name = "users"

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('auth/logout/', views.LogoutView.as_view(), name='token_blacklist'),
    
    
    # User endpoints
    path("users/", views.UserCreateView.as_view(), name="auth_create_user"),
    path("users/<str:id>/", views.UserSpecificDetailView.as_view(), name="get_user_detail"),
    # path("users/<str:id>/", views.DeleteUserView.as_view(), name="delete_user")
    # Vendor endpoints
    
]
