import json
from kavenegar import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from django.core.mail import send_mail

class EmailController(APIView):
    def get(self, request, format=None, *args, **kwargs):
        # def sendNotification(email ,reserve):
        send_mail('subject', 'body of the message', 'notif@sandboxeb808a33cc074adb9fb924eef69c024a.mailgun.org',
                  ['daniel.kamali@yahoo.com', 'daniel.kamali.dk@gmail.com'])
        return Response({}, status=status.HTTP_200_OK)


