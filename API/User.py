
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import ReviewSerializer

from .models import Review,User,Reserves,Business
import json
from .Token import Tokenizer as tokenizer
class UserController(APIView):
    def put(self, request, format=None, *args, **kwargs):
         try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)
            point = float(data['point'])
            description = data['description']
            service_id = data['service_id']


            return Response({}, status=status.HTTP_200_OK)

         except Exception :
             return Response({}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None, *args, **kwargs):
        try:
            user_id = tokenizer.meta_decode(request.META)

            reserves = Reserves.objects.filter(user_id=user_id).order_by('date')

            user =User.objects.get(pk=user_id)

            businseses = Business.objects.filter(owner_id=user_id)

            return Response({'user':{
                'user_name':user.username,
                'full_name':user.first_name+' '+user.last_name
                }
                'reserves':,
                'businseses':

            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


@staticmethod
    def newPointCalculator(service_id,point):
        service = Services.objects.get(pk=service_id)
        service.rating = (service.rating*service.review_count + point)/(service.review_count+1)
        service.review_count = service.review_count + 1
        service.save(force_update=True)
