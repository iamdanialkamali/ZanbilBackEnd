from khayyam import  JalaliDate
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import BusinessSerializer,ServiceSerializer,ReservesSerializer

from .models import Business,Services,Reserves
import json
from .Token import Tokenizer as tokenizer


class DashboardController(APIView):

    def get(self, request, format=None, *args, **kwargs):
        #try:
            id = request.GET['id']
            business=Business.objects.get(pk=id)

            today = JalaliDate.today().__str__()

            #find all reserves for today
            todayReserves=Reserves.objects.filter(service__business__id=business.id , date=today)
            numReservesInDay=len(todayReserves)

            #find all reserves for week
            start_week_date = JalaliDate.today() - timedelta(days=JalaliDate.today().weekday())
            this_week_days_date = []
            weekday_date=start_week_date
            for i in range(7):
                this_week_days_date.append(weekday_date)
                weekday_date = weekday_date + timedelta(1)
            currentWeekReserves=Reserves.objects.filter(service__business__id=business.id , date__in=this_week_days_date)
            numReservesInWeek=len(currentWeekReserves)


            #find all reserves for this mounth
            thisMonthReserves=Reserves.objects.filter(service__business__id=business.id , date__contains=today[:7])
            numReservesInMonth=len(thisMonthReserves)

            #reserves_data=ReservesSerializer(currentWeekReserves,many=True).data

            return Response({
                "numberOfReservesInDay":numReservesInDay,
                "numberOfReservesInCurrentMonth":numReservesInMonth,
                "numberOfReservesInCurrentWeek":numReservesInWeek,
            }, status= status.HTTP_200_OK)

        #except Exception:
         #   return Response({}, status= status.HTTP_400_BAD_REQUEST)



    def patch(self, request, format=None, *args, **kwargs):
         '''
         for editing business
         '''
         try:
            data = json.loads(request.body)
            name = data['name']
            phone_number = data['phone_number']
            email = data['email']
            address = data['address']
            description = data['description']
            category = data['category']
            id = data['id']

            if(True):
                selectedBusiness = Business.objects.get(pk=id)
                selectedBusiness.name = name
                selectedBusiness.phone_number= phone_number
                selectedBusiness.email = email
                selectedBusiness.address = address
                selectedBusiness.description = description
                selectedBusiness.category_id = category
                selectedBusiness.save(force_update=True)

            return Response({}, status=status.HTTP_200_OK)

         except Exception :
             return Response({},status=status.HTTP_400_BAD_REQUEST)
