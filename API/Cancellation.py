import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reserves
import json
from khayyam import *
from .Token import Tokenizer as tokenizer

#cancel the reserve if its not too late
class CancellationController(APIView):
    def post(self, request, format=None, *args, **kwargs):
        try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)
            reserve_id = data['reserve_id']

            if(True):
                selected_Reserve=Reserves.objects.get(pk=reserve_id);

                #check if the user is owner of reservation
                if(user_id!=selected_Reserve.user.id):
                    return Response({"its not your reservation"}, status=status.HTTP_400_BAD_REQUEST)

                #find reservation dateTime
                if(selected_Reserve.date[4]=="/"):
                    reserveDate=selected_Reserve.date.split("/");
                else:
                    reserveDate=selected_Reserve.date.split("-");
                reserveTime=selected_Reserve.sans.start_time.split(":");
                reserveDateTime=JalaliDatetime(int(reserveDate[0]),int(reserveDate[1]),int(reserveDate[2]), int(reserveTime[0]), int(reserveTime[1]),0);

                #find cancellation range
                duration = selected_Reserve.service.cancellation_range.split(":")
                delta = datetime.timedelta(hours=int(duration[0])-1, minutes=int(duration[1]))

                #check isn't it late
                if(JalaliDatetime.now()+delta < reserveDateTime):
                    selected_Reserve.is_cancelled=True
                    selected_Reserve.save(force_update=True)
                    return Response({"done!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"its too late for cancellation"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception :
            return Response({},status=status.HTTP_400_BAD_REQUEST)
