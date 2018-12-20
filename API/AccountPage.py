
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import BusinessSimpleSerializer,ReservesSerializer,UserSerializer

from .models import Review,User,Reserves,Business,Users
import json
from .Token import Tokenizer as tokenizer
class AccountPageController(APIView):

    def get(self, request, format=None, *args, **kwargs):
        try:
            user_id = tokenizer.meta_decode(request.META)

            reserves = Reserves.objects.filter(user_id=user_id).order_by('date')

            user =Users.objects.get(pk=user_id)

            businseses = Business.objects.filter(owner_id=user_id)

            return Response({
                'user':UserSerializer(user).data,
                'reserves':ReservesSerializer(reserves,many=True).data,
                'businseses':BusinessSimpleSerializer(businseses,many=True).data

            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
