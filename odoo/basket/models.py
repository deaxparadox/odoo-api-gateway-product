
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.models import TimeIt
from users.models import ClientUserModel
from product.models import ParentProductModel

class BasketModel(models.Model):
    user_id = models.OneToOneField(
        "users.ClientUserModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("ID of the user owning the basket.")
    )
    line_ids = models.ForeignKey(
        "product.ParentProductModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("List of basket items")
    )
    total_price = models.FloatField(default=0., verbose_name=_("Calculated total price of the basket"))