
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import BusinessSimpleSerializer

from .models import Business
import json
from .Token import Tokenizer as tokenizer
class CategoryController(APIView):

    def get(self, request, format=None, *args, **kwargs):

        try:

            id = request.GET['category_id']
            business=Business.objects.filter(category_id=id)
            business_data=BusinessSimpleSerializer(business,many=True).data
            return Response(business_data, status= status.HTTP_200_OK)

        except Exception:
            return Response({}, status= status.HTTP_400_BAD_REQUEST)


   