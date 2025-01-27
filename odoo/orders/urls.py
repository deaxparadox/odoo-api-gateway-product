from django.urls import path


from .views import OrderView

app_name = "orders"

urlpatterns = [
    # GET: All orders
    # POST: Create a new order.
    path("orders/", OrderView.as_view(), name="get_all_order")
]
