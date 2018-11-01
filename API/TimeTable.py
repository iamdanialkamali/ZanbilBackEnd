
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import BusinessSerializer
import datetime
from datetime import timedelta
from .models import TimeTable,Sans
import json
class TimeTableController(APIView):
    @staticmethod
    def makeTimeTable(days,business_id):

        timeTable = TimeTable.objects.create(business_id=business_id)
        today = datetime.date.today()

        for day in days:
            weekday = 0

            if(day['open']==1):

                start_time = day['start_time'].split(":")

                end_time = day['end_time'].split(":")

                duration = day['duration'].split(":")


                temp_time = datetime.time(hour=int(start_time[0]), minute=int(start_time[1]))
                temp_datetime = datetime.datetime.combine(today, temp_time)

                end_time_obj = datetime.time(hour=int(end_time[0]), minute=int(end_time[1]))
                end_datetime = datetime.datetime.combine(today, end_time_obj)

                rest_start_time = day['rest_start_time'].split(":")
                rest_end_time = day['rest_end_time'].split(":")
                rest_start__time_obj = datetime.time(hour=int(rest_start_time[0]), minute=int(rest_start_time[1]))
                rest_end__time_obj = datetime.time(hour=int(rest_end_time[0]), minute=int(rest_end_time[1]))



                if (day['rest_start_time'] != day['rest_end_time']):
                    rest_start_datetime = datetime.datetime.combine(today, rest_start__time_obj)
                    rest_end_datetime = datetime.datetime.combine(today, rest_end__time_obj)

                else:
                    rest_start_datetime = end_datetime
                    rest_end_datetime = end_datetime

                delta = timedelta(hours=int(duration[0]), minutes=int(duration[1]))

                while(temp_datetime +delta <= end_datetime):
                    if(temp_datetime<rest_end_datetime and temp_datetime>rest_start_datetime):
                        continue
                    else:

                        Sans.objects.create(weekday=weekday,
                                            start_time = temp_datetime.time().__str__()
                                            ,end_time=end_datetime.time().__str__()
                                            ,time_table=timeTable)

                    temp_datetime + delta

            weekday += 1

        return timeTable

#
# start_time = input().split(":")
# ali = datetime.time(hour=int(start_time[0]),minute=int(start_time[1]))
# duration = input().split(":")
#
#
#
#
#
# d = datetime.date.today()
#
# dt = datetime.datetime.combine(d, ali)
#
#
# delta = timedelta(hours=int(duration[0]),minutes=int(duration[1]))
# print(dt + timedelta(hours=int(duration[0]),minutes=int(duration[1])))