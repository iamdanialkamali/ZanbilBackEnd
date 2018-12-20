from django.db.models import Count
from khayyam import  JalaliDate,JalaliDatetime
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import ReservesSerializer

from .models import Review, Services, Sans, Reserves

from .models import Business,Services,Reserves,Users

class DashboardController(APIView):
    def get(self, request, format=None, *args, **kwargs):
        # try:

            business_id = request.GET['id']
            today = JalaliDate.today()
            # reserves = Reserves.objects.filter(service_business__id=business_id)
            #
            # business = Business.objects.get(pk=business_id)

            #find all reserves for today
            numReservesInDay=self.findAllReservesForADay(today,business_id)

            #find all reserves for yesterday
            yesterday = (JalaliDate.today()-timedelta(1)).__str__()
            numReservesInYesterday=self.findAllReservesForADay(yesterday,business_id)

            #calculate increaseReservePercentageForDay
            increaseReservePercentageForDay=0
            if numReservesInYesterday!=0:
                increaseReservePercentageForDay = ((numReservesInDay-numReservesInYesterday)/numReservesInYesterday)*100
            else:
                increaseReservePercentageForDay = 100
            #find all reserves for current week
            numReservesInWeek=self.findAllReservesForAWeek(today,business_id)

            #find all reserves for last week
            numReservesInLastWeek=self.findAllReservesForAWeek(today-timedelta(7),business_id)

            #calculate increaseReservePercentageForWeek
            increaseReservePercentageForWeek=0
            if numReservesInLastWeek!=0:
                increaseReservePercentageForWeek=((numReservesInWeek-numReservesInLastWeek)/numReservesInLastWeek)*100
            else:
                increaseReservePercentageForWeek = 100
            #find all reserves for current mounth
            numReservesInMonth=self.findAllReservesForAMonth(today,business_id)

            #find all reserves for last mounth
            dayInLastMonth=today-timedelta(30)
            numReservesInLastMonth=self.findAllReservesForAMonth(dayInLastMonth,business_id)

            #calculate increaseReservePercentageForMonth
            increaseReservePercentageForMonth=0
            if numReservesInLastMonth!=0:
                increaseReservePercentageForMonth=((numReservesInMonth-numReservesInLastMonth)/numReservesInLastMonth)*100
            else:
                increaseReservePercentageForMonth = 100

            #find popularServices
            popularServices = self.findPopularServices(today,business_id)

            #FIND upcoming reserves
            upcomingReserves=self.getUpcomingReserves(today,business_id)

            #  and all resrves
            allReserves=self.getAllReserves(business_id)

            #customers
            customers=self.findCustomers(business_id)

            #busy sanses
            busySanses=self.findBusySanses(business_id)

            return Response({
                    "increaseReservePercentageForWeek":increaseReservePercentageForWeek,
                    "increaseReservePercentageForMonth":increaseReservePercentageForMonth,
                    "increaseReservePercentageForDay":increaseReservePercentageForDay,
                    "busySanses":busySanses,
                    "customers":customers,
                    "allReservations":allReserves,
                    "upcomingReservations":upcomingReserves,
                    "popularServices":popularServices,
                    "numberOfReservesInDay":numReservesInDay,
                    "numberOfReservesInCurrentMonth":numReservesInMonth,
                    "numberOfReservesInCurrentWeek":numReservesInWeek,
                }, status= status.HTTP_200_OK)


        # except Exception:
        #     return Response({}, status= status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def getAllReserves(business_id):
        allReserves=[]
        services=Services.objects.filter(business__id=business_id)
        for service in services:
            reserves=Reserves.objects.filter(service__id=service.id)
            for reserve in reserves:
                    allReserves.append({
                        "serviceName":service.name,
                        "date":reserve.date,
                        "start_time":reserve.sans.start_time,
                        "end_time":reserve.sans.end_time,
                        })
        allReserves=sorted(allReserves,key=lambda k: k['date'])
        return allReserves


    @staticmethod
    def getUpcomingReserves(day,business_id):
        upcomingReserves=[]
        services=Services.objects.filter(business__id=business_id)

        #now = JalaliDate.today()
        now = JalaliDatetime.now()
        reserves = Reserves.objects.filter(service__business__id=business_id)
        for reserve in reserves:
                splited_date = reserve.date.split('-')
                splited_time = reserve.sans.start_time.split(':')
                reserve_time = JalaliDatetime(
                    int(splited_date[0]),
                    int(splited_date[1]),
                    int(splited_date[2]),
                    int(splited_time[0]),
                    int(splited_time[1]),
                    0
                )

                if(reserve_time > now):
                    upcomingReserves.append(
                        ReservesSerializer(reserve).data
                    )

                # isComing=False
                # #next years
                # if int(reserve.date[:4])>int(todayS[:4]):
                #     isComing=True
                # #next months in same year
                # elif int(reserve.date[:4])==int(todayS[:4]) and int(reserve.date[5:7])>int(todayS[5:7]):
                #     isComing=True
                #     #next days in same month
                # elif int(reserve.date[:4])==int(todayS[:4]) and int(reserve.date[5:7])==int(todayS[5:7]) and int(reserve.date[8:])>=int(todayS[8:]):
                #     isComing=True
                # if isComing :

                # upcomingReserves.append({
                #     "serviceName": reserve.,
                #     "date": reserve.date,
                #     "start_time": reserve.sans.start_time,
                #     "end_time": reserve.sans.end_time,
                # })




        upcomingReserves=sorted(upcomingReserves,key=lambda k: k['date'])
        return upcomingReserves

    @staticmethod
    def findAllReservesForADay(day,business_id):
        todayReserves=Reserves.objects.filter(service__business__id=business_id , date=day)
        numReservesInDay=len(todayReserves)
        return numReservesInDay

    @staticmethod
    def findAllReservesForAMonth(day,business_id):
        day=day.__str__()
        currentMonthReserves=Reserves.objects.filter(service__business__id=business_id , date__contains=day[:7])
        numReservesInMonth=len(currentMonthReserves)
        return numReservesInMonth

    @staticmethod
    def  findAllReservesForAWeek(day,business_id):
        start_week_date = day - timedelta(days=JalaliDate.today().weekday())
        this_week_days_date = []
        weekday_date=start_week_date
        for i in range(7):
            this_week_days_date.append(weekday_date)
            weekday_date = weekday_date + timedelta(1)
        currentWeekReserves=Reserves.objects.filter(service__business__id=business_id , date__in=this_week_days_date)
        numReservesInWeek=len(currentWeekReserves)
        return numReservesInWeek


    @staticmethod
    def findPopularServices(day,business_id):
        popularServices=[]
        services=Services.objects.filter(business__id=business_id)
        for service in services:
            Tname=service.name
            dayS=day.__str__()
            cMonthRes=Reserves.objects.filter(service__id=service.id , date__contains=dayS[:7])
            TnumberOfReservesInCurrentMonth=len(cMonthRes)
            start_week_date = day - timedelta(days=JalaliDate.today().weekday())
            this_week_days_date = []
            weekday_date=start_week_date
            for i in range(7):
                this_week_days_date.append(weekday_date)
                weekday_date = weekday_date + timedelta(1)
            cWeekRes=Reserves.objects.filter(service__id=service.id , date__in=this_week_days_date)
            TnumberOfReservesInCurrentWeek=len(cWeekRes)
            popularServices.append({
                    "name":Tname,
                    "numberOfReservesInCurrentMonth":TnumberOfReservesInCurrentMonth,
                    "TnumberOfReservesInCurrentWeek":TnumberOfReservesInCurrentWeek
                })
            popularServices = sorted(popularServices, key=lambda k: k['numberOfReservesInCurrentMonth'],reverse=True)
            return popularServices[0:3]

    @staticmethod
    def findCustomers(business_id):
        customers=[]
        customers_ids=Reserves.objects.filter(service__business__id=business_id).values_list('user', flat=True)
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
        return customers

    @staticmethod
    def findBusySanses(business_id):
        sanses = Reserves.objects.filter(sans__reserves__service__business_id=business_id).values('sans_id')
        sanses = sanses.annotate(Count('sans_id'))
        sanses_ids = []
        for sans in sanses:
            sanses_ids.append(sans['sans_id'])
        sans_objects = Sans.objects.filter(id__in=sanses_ids)
        busySanses = []
        for sans in sans_objects.values():
            temp_sans = sans
            temp_sans['count'] = sanses.get(sans_id=sans['id'])['sans_id__count']  ##addes Count
            busySanses.append(temp_sans)
        return busySanses
