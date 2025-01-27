from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from helpers.models import TimeIt

class NotificationStatusChoices(models.IntegerChoices):
    SENT = 0
    PENDING = 1
    FAILED = 2

class NotificationModel(TimeIt):
    title = models.CharField(max_length=120, verbose_name=_("Title of the notification."))
    body = models.CharField(max_length=255, verbose_name=_("Main content of the notification"))
    client_user = models.ManyToManyField(
        "users.ClientUserModel",
        verbose_name=_("List of users the notification is sent to"),
        related_name="notifications"
    )
    vendor_user = models.ManyToManyField(
        "users.VendorsModel",
        verbose_name=_("List of notification for the vendor"),
        related_name="notifications"
    )
    status = models.IntegerField(
        default=NotificationStatusChoices.PENDING,
        verbose_name=_("Status of the application")
    )