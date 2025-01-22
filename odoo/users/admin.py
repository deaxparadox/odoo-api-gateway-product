from django.contrib import admin
from users.models import ClientUserModel

@admin.register(ClientUserModel)
class ClientUserAdmin(admin.ModelAdmin):
    pass