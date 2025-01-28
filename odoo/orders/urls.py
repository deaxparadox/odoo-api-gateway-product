from django.urls import path


from .views import OrderView, OrderDetails

app_name = "orders"

urlpatterns = [
    # GET: All orders
    # POST: Create a new order.
    path("orders/", OrderView.as_view(), name="get_all_order"),
    
    # GET: Get defails of a specific order.
    # PUT: Update an order, change payment method
    # DELETE: Cancel an order.
    path("orders/<str:order_id>/", OrderDetails.as_view(), name="order_update")
]
