
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.models import TimeIt
from users.models import ClientUserModel
from product.models import ParentProductModel

class BasketModel(models.Model):
    # change user_id (docs) to user (for clarity)
    user = models.OneToOneField(
        "users.ClientUserModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("ID of the user owning the basket."),
        related_name="basket"
    )
    # line_ids = models.ManyToManyField(
    #     "product.ParentProductModel",
    #     verbose_name=_("List of basket items"),
    #     related_name="basket"
    # )
    total_price = models.FloatField(default=0., verbose_name=_("Calculated total price of the basket"))
    
    def set_total_price(self):
        """
        - Update the total price of the basket item and save them.
        - Set the total price of basket.
        
        `Instace must be saved after calling this method to update the total price of basket`.
        """
        
        total = 0.
        for item in self.basket_item.all():
            item.set_total_price()
            item.save()
            total+=item.total_price
        self.total_price = total
    
class BasketItem(models.Model):
    basket_id = models.ForeignKey(
        BasketModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Basket items"),
        related_name="basket_item"
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name=_("Quantity")
    )
    product_id = models.ForeignKey(
        "product.ProductVariantsModel",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("List of Products"),
        related_name="basket_item"
    )
    total_price = models.FloatField(
        default=0.0,
        verbose_name=_("Total price of basket item")
    )
    
    def set_total_price(self):
        self.total_price = float(self.quantity) * self.product_id.get_total_price()