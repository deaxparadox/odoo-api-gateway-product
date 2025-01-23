from django.urls import path

from . import views

app_name = "basket"

urlpatterns = [
    path("basket/", views.BasketView.as_view(), name="user_current_basket"),
    path("basket/items/", views.BasketItem.as_view(), name="user_basket_item"),
]
