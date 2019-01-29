import json

from khayyam import JalaliDate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .Notification import NotificationController
from .Serializer import *
from .Token import Tokenizer as tokenizer
from passlib.hash import pbkdf2_sha256  as decryptor


class ReserveController(APIView):
    def put(self, request, format=None, *args, **kwargs):

        try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)
            description = data['description']
            sans_id = data['sans_id']
            service_id = data['service_id']
            date = data['date']
            sans = Sans.objects.get(pk=sans_id)

            service = Services.objects.get(pk = service_id)
            if(service.is_protected):
                password = data['password']
                verified = decryptor.verify(password,service.password)
            reserves = Reserves.objects.filter(sans_id=sans_id,
                                            date=date,
                                            service_id=service_id,
                                            is_cancelled=False).values()
            free = len(reserves) < sans.capacity
            if ( free and verified):

                reserve = Reserves.objects.create(user_id=user_id,
                                                  description=description,
                                                  sans_id=sans_id,
                                                  date=date,
                                                  service_id=service_id,
                                                  )
                # NotificationController.Notify(user_id,sans_id,date)
                reserve_data = ReservesSerializer(reserve).data
                return Response(reserve_data
                            , status=status.HTTP_200_OK)

            else:
                raise Exception

        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
