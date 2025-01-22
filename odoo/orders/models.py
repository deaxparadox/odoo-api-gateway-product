from django.db import models
from django.utils.translation import gettext_lazy as _

class Basket:
    user_id = models.OneToOneField(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("ID of the user owning the basket.")
    )
    line_ids = models