
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import BusinessSimpleSerializer,ReservesSerializer,UserSerializer

from .models import Review,User,Reserves,Business,Users
import json
from .Token import Tokenizer as tokenizer

from khayyam import *
import datetime
import json


class AccountPageController(APIView):

    def get(self, request, format=None, *args, **kwargs):
        try:
            user_id = tokenizer.meta_decode(request.META)

            reserves = Reserves.objects.filter(user_id=user_id).order_by('date')
            reserves_list = []
            for reserve in reserves:
                if(reserve.date[4]=="/"):
                    reserveDate=reserve.date.split("/");
                else:
                    reserveDate=reserve.date.split("-");
               
                reserveTime=reserve.sans.start_time.split(":");
                
                reserveDateTime=JalaliDatetime(int(reserveDate[0]),int(reserveDate[1]),int(reserveDate[2]), int(reserveTime[0]), int(reserveTime[1]),0);

                #find cancellation range
                duration = reserve.service.cancellation_range.split(":")
                delta = datetime.timedelta(hours=int(duration[0])-1, minutes=int(duration[1]))

                #check isn't it late
                if(JalaliDatetime.now() + delta < reserveDateTime):
                    reserve = {
                        'reserve':ReservesSerializer(reserve).data,
                        'is_cancellabe':True
                    }
                else:
                    reserve = {
                        'reserve':ReservesSerializer(reserve).data,
                        'is_cancellabe':False
                    }
                    reserves_list.append(reserve)


            user =Users.objects.get(pk=user_id)

            businseses = Business.objects.filter(owner_id=user_id)

            return Response({
                'user':UserSerializer(user).data,
                'reserves':reserves_list,
                'businseses':BusinessSimpleSerializer(businseses,many=True).data

            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
