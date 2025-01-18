from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeIt(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date of creation"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Access date"))
    
    class Meta:
        abstract = True