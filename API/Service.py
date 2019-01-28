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
from rest_framework.parsers import MultiPartParser

from passlib.hash import pbkdf2_sha256  as encryptor

class ServiceController(APIView):
    parser_classes = (MultiPartParser,)

    def put(self, request, format=None, *args, **kwargs):

        # try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)
            name = data['name']
            description = data['description']
            price = data['price']
            business_id = data['business_id']
            days = data['days']
            is_protected =  data['is_protected']
            password =  data['password']
            
            is_protected = bool(int(is_protected))

            hased_pass = encryptor.encrypt(password, rounds=2000, salt_size= 16)
            timetable = TimeTableController.makeTimeTable(days,business_id)
            
            if(True):
                myService = Services.objects.create(
                    name = name,
                    description=description,
                    fee=price,
                    business_id=business_id,
                    rating=10,
                    timetable_id=timetable.id,
                    is_protected = is_protected,
                    password = hased_pass
                )

            
            sanses = SansController.getSansForWeek(timetable.id)


            service_data = ServiceSerializer(myService).data

            return Response({'service':service_data,
                            'timetable' : sanses}
                                , status=status.HTTP_200_OK)
        # except Exception :
        #     return Response({},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None, *args, **kwargs):
        try:
            id = request.GET['service_id']
            service=Services.objects.get(id=id)
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

    def patch(self, request, format=None, *args, **kwargs):

        '''
                for editing service
                get name description fee and
                sanses(start_time,end_time,sans_id,is_deleted) as json
                '''
        try:
            data = json.loads(request.body)
            name = data['name']
            description = data['description']
            fee = data['fee']
            sanses = data['sanses']
            id = data['id']
            
            old_password = data['old_password']
            new_password = data['new_password']

            # edit name and fee and description
            selectedService = Services.objects.get(pk=id)
            selectedService.name = name
            selectedService.fee = fee
            selectedService.description = description
            
            if( not old_password==""):
                valid = encryptor.verify(old_password,selectedSans.password)
                if(valid):
                    selectedService.password = encryptor.encrypt(new_password, rounds=2000, salt_size= 16)
            selectedService.save(force_update=True)

            # edit sanses
            for sans in sanses:
                selectedSans = Sans.objects.get(pk=sans['sans_id'])
                if sans['is_deleted'] == "1":
                    selectedSans.delete()
                else:
                    selectedSans.capacity = sans['capacity']
                    selectedSans.start_time = sans['start_time']
                    selectedSans.end_time = sans['end_time']
                    selectedSans.save(force_update=True)
            return Response({}, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

class SearchController(APIView):
    def post(self, request, format=None, *args, **kwargs):
        try:
            data = json.loads(request.body)
            service_name = data['service_name']
            business_name = data['business_name']
            min_price = data['min_price']
            max_price = data['max_price']
            category = data['category']
            search = False

            for i in data.values() :
                if i !='':
                    search = True

            if(search):
                serivce_list = Services.objects

            else:
                return Response([], status=status.HTTP_200_OK)





            if (service_name!=''):
                serivce_list = serivce_list.filter(
                    name=service_name
                )

            if (business_name!=''):
                serivce_list = serivce_list.filter(
                    business__name__contains= business_name
                )

            if (min_price!=''):
                min_price = int(min_price)
                serivce_list = serivce_list.filter(
                    fee__gte=min_price
                )
            if(max_price!= ''):
                max_price = int(max_price)
                serivce_list = serivce_list.filter(fee__lte=max_price)
            if (category!=''):
                category = int(category)
                serivce_list = serivce_list.filter(
                    business__category__id__exact=category
                )
            serivce_data = ServiceSearchSerializer(serivce_list,many=True).data
            return Response(serivce_data, status=status.HTTP_200_OK)

        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)