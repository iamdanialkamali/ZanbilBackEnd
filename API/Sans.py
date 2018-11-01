from khayyam import  JalaliDate
from datetime import timedelta
from .models import Sans,Reserves
from .Serializer import SansSerializer

class SansController:
    @staticmethod
    def getSansForWeek(timetable_id):
        sanses = Sans.objects.filter(timetable__id=timetable_id)
        result = [[],[],[],[],[],[],[]]
        for sans in sanses :
            serialized = SansSerializer(sans)
            result[sans.weekday].append(serialized.data)
    #get date and timetable id and return
        return result
    @staticmethod
    def getSansForPage(timetable_id,date):

        #calculate weekdays date of given date
        date_splited = date.split('/')
        Jdate = JalaliDate(int(date_splited[0]), int(date_splited[1]), int(date_splited[2]))
        start_week_date = Jdate - timedelta(days=Jdate.weekday())

        # make a list of weekdays date in our format
        this_week_days_date = []
        weekday_date=start_week_date;
        for i in range(7):
            weekday_date.__str__().replace('-', '/')
            this_week_days_date.append(weekday_date.__str__().replace('-', '/'))
            weekday_date = weekday_date + timedelta(1)

        #get sanses
        selected_sanses = Sans.objects.filter(
            time_table__id=timetable_id).order_by('start_time')

        # get reserved sanses in given week
        reserved_sanses = Reserves.objects.filter(date__in=this_week_days_date)

        #exmine are seleted sanses reserved
        result=[[],[],[],[],[],[],[]]
        for sans in selected_sanses:
                is_reserved = False
                for reserved in reserved_sanses:
                    if (sans.id == reserved.sans.id):
                        is_reserved = True
        result[sans.weekday].append({"sans":sans,"is_reserved": is_reserved});

        return result
