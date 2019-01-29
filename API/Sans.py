from khayyam import  JalaliDate
from datetime import timedelta
from .models import Sans,Reserves
from .Serializer import SansSerializer

from django.db.models import Count


class SansController:
    @staticmethod
    def getSansForWeek(timetable_id):
        sanses = Sans.objects.filter(timetable__id=timetable_id)
        result = [[],[],[],[],[],[],[]]
        for sans in sanses :
            serialized = SansSerializer(sans)
            result[sans.weekday].append(serialized.data)
        return result

    # get date and timetable id and return sanses
    @staticmethod
    def getSansForPage(timetable_id,date):

        #calculate weekdays date of given date
        date_splited = date.split('/')
        Jdate = JalaliDate(int(date_splited[0]), int(date_splited[1]), int(date_splited[2]))
        start_week_date = Jdate - timedelta(days=Jdate.weekday())
        today_weekday = JalaliDate.today().weekday()
        # make a list of weekdays date in our format
        this_week_days_date = []
        weekday_date=start_week_date
        for i in range(7):
            this_week_days_date.append(weekday_date.__str__().replace('-', '/'))
            weekday_date = weekday_date + timedelta(1)

        #get sanses
        selected_sanses = Sans.objects.filter(
            timetable__id=timetable_id).order_by('start_time')

        # get reserved sanses in given week
        # reserved_sanses = Reserves.objects.filter(date__in=this_week_days_date)
        reserved_sanses = Reserves.objects.filter(date__in=this_week_days_date)
        #exmine are seleted sanses reserved
        
        reserved_sanses = Reserves.objects.filter(date__in=this_week_days_date).values('sans_id').annotate(total=Count('sans_id')).order_by('total')

               
        result=[[],[],[],[],[],[],[]]
        for sans in selected_sanses:
            is_reserved = False
            if(start_week_date < JalaliDate.today()-timedelta(today_weekday)):
                is_reserved = True

            elif(start_week_date == JalaliDate.today()-timedelta(today_weekday) and  sans.weekday<today_weekday  ):
                is_reserved = True
            capacity = sans.capacity - len(reserved_sanses.filter(sans_id = sans.id ).values())
            
            if(capacity<1):
                is_reserved = True
            result[sans.weekday].append({"sans":SansSerializer(sans).data,"is_reserved": is_reserved , 'capacity':capacity})

        return (result,start_week_date.__str__().replace('-','/'))



