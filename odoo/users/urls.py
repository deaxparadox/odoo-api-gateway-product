from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserCreateView, UserSpecificDetailView, UserLoginPairView

app_name = "users"

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', UserLoginPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    # User endpoints
    path("users/", UserCreateView.as_view(), name="auth_create_user"),
    path("users/<str:id>/", UserSpecificDetailView.as_view(), name="get_user_detail")
    # Vendor endpoints
    
]
