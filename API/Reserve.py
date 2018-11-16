import json

from khayyam import JalaliDate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .Sans import SansController
from .models import Reserves
from .Serializer import *
from .TimeTable import TimeTableController
from .Token import Tokenizer as tokenizer
from .models import Services


class ReserveController(APIView):
    def put(self, request, format=None, *args, **kwargs):

        try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)

            """
             user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    service = models.ForeignKey(to=Services, on_delete=models.DO_NOTHING, null=True)
    sans = models.ForeignKey(Sans, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField()
    date = models.CharField(max_length=150)
            """

            description = data['description']
            sans_id = data['sans_id']
            service_id = data['service_id']
            date = data['date']
            
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

