from kavenegar import *

from django.core.mail import send_mail

class EmailController(APIView):
    @staticmethod
    def sendNotification(email ,data):
        message = "Your Resreve Has been set on\n " + data.date + "\n " +data.time
        send_mail('Notification', message, 'notif@sandboxeb808a33cc074adb9fb924eef69c024a.mailgun.org',
                  ['daniel.kamali@yahoo.com', email])
        return 1


class SMSController:
    @staticmethod
    def sendNotification(number,data):
        message = "Your Resreve Has been set on\n " + data.date + "\n " +data.time
        api = KavenegarAPI('434D634935754F355537366E526570396666524B41584A61752F426F79415944')
        params = {
            'sender': '100065995',
            'receptor': number,
            'message' : message
        }
        api.sms_send(params)
        return 1