from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.IntegerChoices):
    DRAFT = 0
    CONFIRMED = 1
    DONE = 2

class OrderModel(models.Model):
    id = models.CharField(max_length=10, primary_key=True, verbose_name=_("Unique identifier of the order"))
    name = models.CharField(max_length=120, null=True, verbose_name=_("Order reference"))
    user_id = models.OneToOneField(
        "users.ClientUserModel",
        verbose_name=_("ID of the customer who place the order"),
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.IntegerField(default=OrderStatus.DRAFT, choices=OrderStatus, verbose_name=_("Status of the order"))
    order_date = models.DateField(auto_now_add=True)
    total_price = models.FloatField(verbose_name=_("Total amount of the order"))
    shipping_address = models.OneToOneField(
        "users.AddressModel",
        verbose_name=_("Shipping address linked to the order"),
        on_delete=models.SET_NULL,
        null=True
    )