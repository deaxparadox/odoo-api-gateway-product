from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class OdooUserAbstract(models.Model):
    # Email is required for user_id
    user_id = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="Full identifier of the user"
    )
    phone = models.BigIntegerField(default=0000000000, null=True, blank=True, verbose_name="Phone number")
    address = models.CharField(default="", max_length=255, blank=True, null=True, verbose_name="Shipping/billing address")
    is_company = models.BooleanField(default=False)
    # is_active is Implemented in `auth_user`
    
    class Meta:
        abstract = True

class ClientUserModel(OdooUserAbstract):
    # username, password, and email will be create 
    # on django Models
    auth_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_user"
    )
    pass 

class VendorsModel(OdooUserAbstract):
    name = models.CharField(max_length=120, verbose_name="Full name of the user.")
    email = models.EmailField(_("email address"), blank=True)