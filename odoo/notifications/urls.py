from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    # GET:  Get all notifiations
    # POST: Create a new notificatoins
    path("notifications/", views.NotificationsView.as_view(), name="get_all_notifications")
]
