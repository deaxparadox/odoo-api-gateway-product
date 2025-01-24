from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from helpers import create_variable_hash

@receiver(post_save, sender=User)
def create_client_user_for_admin(sender, **kwargs):
    instance = kwargs['instance']
    if instance.is_superuser:
        if len(instance.email) == 0:
            print(
                f"\n\tUnable to create ClientUserModel for superuser {instance.username}"
                "\n\tUser doesnot provided email."
                "\n\n\tContact admin\n"
            )
        else:
            ClientUserModel.objects.create(
                user_id=create_variable_hash(instance.email),
                auth_user=instance
            )
            print(f'\n\tClientUserModel created for superuser {instance}\n')
        
        
        


class OdooUserAbstract(models.Model):
    # Email is required for user_id
    user_id = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="Full identifier of the user"
    )
    phone = models.BigIntegerField(default=0000000000, null=True, blank=True, verbose_name="Phone number")
    # address = models.CharField(default="", max_length=255, blank=True, null=True, verbose_name="Shipping/billing address")
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
    

class VendorsModel(OdooUserAbstract):
    auth_user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="client_vendor"
    )
    
    
    
class AddressModel(models.Model):
    user_id = models.ForeignKey(
        ClientUserModel,
        verbose_name=_("Client user addresss"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="address"
    )
    vendor_id = models.ForeignKey(
        VendorsModel,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Vendor user address"),
        related_name="address"
    )
    address1 = models.CharField(max_length=255, verbose_name=_("Street name, locality"))
    address2 = models.CharField(max_length=255, verbose_name=_("Landmark"), null=True, blank=True)
    state = models.CharField(max_length=120, verbose_name=_("State of location"))
    country = models.CharField(max_length=60, verbose_name=_("Country of Location"))