from rest_framework import serializers
from .models import NotificationModel, NotificationStatusChoices

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = ['title', 'body']