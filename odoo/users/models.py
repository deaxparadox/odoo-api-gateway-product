from django.db import models
from django.contrib.auth.models import User


class ClientUserModel(models.Model):
    # Email is required for user_id
    user_id = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="Full identifier of the user"
    )
    # username, password, and email will be create 
    # on django Models
    auth_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_user"
    )
    phone = models.BigIntegerField(null=True, blank=True, verbose_name="Phone number")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Shipping/billing address")
    is_company = models.BooleanField(default=False, )
    
    # is_active is Implemented in `auth_user`