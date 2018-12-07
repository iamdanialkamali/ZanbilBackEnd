from django.db.models import Count
from khayyam import  JalaliDate
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Review, Services, Sans, Reserves

from .models import Business,Services,Reserves,Users


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
            currentMonthReserves=Reserves.objects.filter(service__business__id=business.id , date__contains=today[:7])
            numReservesInMonth=len(currentMonthReserves)


            #find popularServices
            popularServices=[]
            services=Services.objects.filter(business__id=business.id)
            for service in services:
                Tname=service.name
                cMonthRes=Reserves.objects.filter(service__id=service.id , date__contains=today[:7])
                TnumberOfReservesInCurrentMonth=len(cMonthRes)
                cWeekRes=Reserves.objects.filter(service__id=service.id , date__in=this_week_days_date)
                TnumberOfReservesInCurrentWeek=len(cWeekRes)
                popularServices.append({
                    "name":Tname,
                    "numberOfReservesInCurrentMonth":TnumberOfReservesInCurrentMonth,
                    "TnumberOfReservesInCurrentWeek":TnumberOfReservesInCurrentWeek
                })
                popularServices = sorted(popularServices, key=lambda k: k['numberOfReservesInCurrentMonth'],reverse=True)

            #FIND coming reserves and all resrves
            upcomingReserves=[]
            allReserves=[]
            for service in services:
                reserves=Reserves.objects.filter(service__id=service.id)
                for reserve in reserves:
                         isComing=False
                        #next years
                         if int(reserve.date[:4])>int(today[:4]):
                            isComing=True
                        #next months in same year
                         elif int(reserve.date[:4])==int(today[:4]) and int(reserve.date[5:7])>int(today[5:7]):
                            isComing=True
                        #next days in same month
                         elif int(reserve.date[:4])==int(today[:4]) and int(reserve.date[5:7])==int(today[5:7]) and int(reserve.date[8:])>=int(today[8:]):
                            isComing=True
                         if isComing :
                            upcomingReserves.append({
                            "serviceName":service.name,
                            "date":reserve.date,
                            "start_time":reserve.sans.start_time,
                            "end_time":reserve.sans.end_time,
                            })
                         allReserves.append({
                            "serviceName":service.name,
                            "date":reserve.date,
                            "start_time":reserve.sans.start_time,
                            "end_time":reserve.sans.end_time,
                            })
            upcomingReserves=sorted(upcomingReserves,key=lambda k: k['date'])
            allReserves=sorted(allReserves,key=lambda k: k['date'])

            #customers
            customers=[]
            customers_ids=Reserves.objects.filter(service__business__id=business.id).values_list('user', flat=True)
            customers_ids=set(customers_ids)
            for id in customers_ids:
                customer=Users.objects.get(pk=id)
                customers.append(
                    {
                        "firstname":customer.first_name,
                        "lastname":customer.last_name,
                        "Email":customer.email,
                        "phone_number":customer.phone_number
                    }
                )





            sanses = Reserves.objects.filter(sans__reserves__service__business=business).values('sans_id')
            sanses = sanses.annotate(Count('sans_id'))

            sanses_ids = []
            for sans in sanses:
                sanses_ids.append(sans['sans_id'])
            sans_objects = Sans.objects.filter(id__in=sanses_ids)
            final_list = []
            for sans in sans_objects.values():
                temp_sans = sans

                temp_sans['count'] = sanses.get(sans_id=sans['id'])['sans_id__count']  ##addes Count
                final_list.append(temp_sans)
            
            return Response({
                    "customers":customers,
                    "allReservations":allReserves,
                    "upcomingReservations":upcomingReserves,
                    "popularServices":popularServices,
                    "numberOfReservesInDay":numReservesInDay,
                    "numberOfReservesInCurrentMonth":numReservesInMonth,
                    "numberOfReservesInCurrentWeek":numReservesInWeek,
                }, status= status.HTTP_200_OK)


        #except Exception:
         #   return Response({}, status= status.HTTP_400_BAD_REQUEST)
