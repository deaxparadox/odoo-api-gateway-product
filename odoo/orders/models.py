from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.generate import generate_random_string

class OrderStatus(models.IntegerChoices):
    DRAFT = 0
    CONFIRMED = 1
    DONE = 2

class OrderModel(models.Model):
    order_id = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name=_("Unique identifier of the order"),
        unique=True,
        default=generate_random_string,
    )
    name = models.CharField(max_length=120, null=True, verbose_name=_("Order reference"))
    user_id = models.ForeignKey(
        "users.ClientUserModel",
        verbose_name=_("ID of the customer who place the order"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders"
    )
    status = models.IntegerField(default=OrderStatus.DRAFT, choices=OrderStatus, verbose_name=_("Status of the order"))
    order_date = models.DateField(auto_now_add=True)
    total_price = models.FloatField(verbose_name=_("Total amount of the order"))
    shipping_address = models.ForeignKey(
        "users.AddressModel",
        verbose_name=_("Shipping address linked to the order"),
        on_delete=models.SET_NULL,
        null=True
    )
    
class OrderLinesModel(models.Model):
    line_id = models.CharField(
        primary_key=True,
        max_length=10,
        verbose_name=_("ID of the parent order"),
        unique=True,
        default=generate_random_string,
    )
    order_id = models.ForeignKey(
        "orders.OrderModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("ID of the parent order"),
        related_name="order_line"
    )
    product_id = models.ForeignKey(
        "product.ProductVariantsModel",
        verbose_name=_("Id of the product ordered"),
        related_name="order_line",
        null=True,
        on_delete=models.SET_NULL
    )
    product_uom_qty = models.IntegerField(
        verbose_name=_("Quantity of the product ordered")
    )
    price_unit = models.FloatField(
        verbose_name=_("Unit price of the product")
    )
    subtotal = models.FloatField(
        verbose_name=_("Subtotal amount for the line")
    )