import json

from khayyam import JalaliDate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .Notification import EmailController,SMSController
from .Serializer import *
from .Token import Tokenizer as tokenizer


class ReserveController(APIView):
    def put(self, request, format=None, *args, **kwargs):

        try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)
            description = data['description']
            sans_id = data['sans_id']
            service_id = data['service_id']
            date = data['date']

            if (len(Reserves.objects.filter(sans_id=sans_id,
                                            date=date,
                                            service_id=service_id).values()) == 0):

                reserve = Reserves.objects.create(user_id=user_id,
                                                  description=description,
                                                  sans_id=sans_id,
                                                  date=date,
                                                  service_id=service_id)
                SMSController.Notify(user_id,sans_id,date)
            else:
                raise Exception
            reserve_data = ReservesSerializer(reserve).data
            return Response(reserve_data
                            , status=status.HTTP_200_OK)

        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
