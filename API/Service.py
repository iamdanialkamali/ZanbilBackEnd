import json

from khayyam import JalaliDate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .Sans import SansController
from .Serializer import *
from .TimeTable import TimeTableController
from .Token import Tokenizer as tokenizer
from .models import Services


class ServiceController(APIView):
    def put(self, request, format=None, *args, **kwargs):

        try:
            user_id = tokenizer.meta_decode(request.META)
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

            sanses,start_week_date = SansController.getSansForWeek(timetable.id)


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
            Services.objects.get().filter('')
            service_data=ServiceSerializer(service).data
            timetable = TimeTable.objects.get(services__id=service.id)
            today = JalaliDate.today().__str__().replace('-','/')
            sanses,start_of_week_date = SansController.getSansForPage(timetable_id=timetable.id,date=today)

            return Response({"service":service_data,
                             "sanses":sanses,
                             "start_of_week_date":start_of_week_date},
                            status= status.HTTP_200_OK)

        except Exception:
           return Response({}, status= status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None, *args, **kwargs):
        try:
            data = json.loads(request.body)
            date = data['date']
            id = data['service_id']
            service = Services.objects.get(pk=id)
            service_data=ServiceSerializer(service).data
            # id = request.POST['service_id']

            timetable = TimeTable.objects.get(services__id=service.id)
            (sanses,start_of_week_date) =SansController.getSansForPage(timetable_id=timetable.id,date=date)

            return Response({"service": service_data,
                             "sanses": sanses,
                             "start_of_week_date":start_of_week_date}
                            , status=status.HTTP_200_OK)
        except Exception:
             return Response({}, status= status.HTTP_400_BAD_REQUEST)


class SearchController(APIView):
    def post(self, request, format=None, *args, **kwargs):
        # try:
            data = json.loads(request.body)
            service_name = data['service_name']
            business_name = data['business_name']
            min_price = data['min_price']
            max_price = data['max_price']
            category = data['category']
            serivce_list = Services.objects.select_related()

            if (service_name!=''):
                serivce_list = serivce_list.filter(
                    name=service_name
                )

            if (business_name!=''):
                serivce_list = serivce_list.filter(
                    business__name__contains= business_name
                )

            if (min_price!='' and max_price!=''):
                min_price = int(min_price)
                max_price = int(max_price)
                serivce_list = serivce_list.filter(
                    fee__range=[min_price,max_price]
                )
            if (category!=''):
                category = int(category)
                serivce_list = serivce_list.filter(
                    business__category__id__exact=category
                )
            serivce_data = ServiceSearchSerializer(serivce_list,many=True).data
            return Response(serivce_data, status=status.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status=status.HTTP_400_BAD_REQUEST)