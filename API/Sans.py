from .models import Sans
from .Serializer import SansSerializer

class SansController:
    @staticmethod
    def getSansForWeek(timetable_id):
        sanses = Sans.objects.filter(time_table__id=timetable_id)
        result = [[],[],[],[],[],[],[]]
        for sans in sanses :
            serialized = SansSerializer(sans)
            result[sans.weekday].append(serialized.data)

    @staticmethod
    def getSansForPage(timetable_id,date):
        return 0