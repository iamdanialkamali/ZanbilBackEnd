
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import *

from .models import Services
import json
from .Token import Tokenizer as tokenizer
from .TimeTable import TimeTableController
from .Sans import SansController

class ServiceController(APIView):
    def put(self, request, format=None, *args, **kwargs):

        try:
            user_id = tokenizer.meta_encode(request.META)
            data = json.loads(request.body)
            name = data['name']
            description = data['description']
            price = data['price']
            business_id = data['business_id']
            days = data['days']

            timetable = TimeTableController.makeTimeTable(days,business_id)

            if(True):
                myService = Services.objects.create(
                    name = name,
                    description=description,
                    fee=price,
                    business_id=business_id,
                    rating=10,
                    timetable=timetable,
                )

            sanses = SansController.getSansForWeek(timetable.id)

            service_data = ServiceSerializer(myService).data
            return Response({'service':service_data,
                            'timetable' : sanses}
                                , status=status.HTTP_200_OK)
        except Exception :
            return Response({},status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None, *args, **kwargs):
        try:
            id = request.GET['service_id']
            service=Services.objects.get(pk=id)
            service_data=ServiceSerializer(service).data
            return Response(service_data, status= status.HTTP_200_OK)

        except Exception:
            return Response({}, status= status.HTTP_400_BAD_REQUEST)


    def patch(self, request, format=None, *args, **kwargs):
        pass
