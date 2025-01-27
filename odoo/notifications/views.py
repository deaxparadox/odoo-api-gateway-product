from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import NotificationModel, NotificationStatusChoices
from .serializers import NotificationsSerializer

class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_notifications(self, client):
        """
        Return all the pending message for the particular client,
        and update the status to SENT.
        """
        notifies = client.notifications.filter(status=NotificationStatusChoices.PENDING)
        for notes in notifies:
            notes.status = NotificationStatusChoices.SENT
            notes.save()
        return notifies
    
    def get(self, request):
        """
        Return the all the PENDING notifications.
        
        - Get the user instance from request.
        - Check the user type and return their messages.
        - Update PENDING messages status to SENT
        """
        try:
            # check user type
            if hasattr(request.user, "client_user"):
                print("getting user notifications")
                serializer = NotificationsSerializer(
                    self.get_notifications(request.user.client_user), many=True
                )
                return Response({"Message": serializer.data}, status=status.HTTP_200_OK)
            if hasattr(request.user, 'client_vendor'):
                print("getting vendor notifications")
                serializer = NotificationsSerializer(
                    self.get_notifications(request.user.client_vendor), many=True
                )
                return Response({"Message": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)