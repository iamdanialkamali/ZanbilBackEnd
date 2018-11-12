
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import BusinessSerializer

from .models import Business
import json
from .Token import Tokenizer as tokenizer
class BusinessController(APIView):
    def put(self, request, format=None, *args, **kwargs):
            # user_id = tokenizer.meta_encode(request.META)


         try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)
            name = data['name']
            phone_number = data['phone_number']
            email = data['email']
            address = data['address']
            description = data['description']
            category = data['category']

            if(True):
                mybusiness = Business.objects.create(
                    owner_id = user_id,
                    name = name,
                    phone_number= phone_number,
                    email = email,
                    address = address,
                    description = description,
                    category_id = category

                )

            business_data = BusinessSerializer(mybusiness).data
            return Response(business_data, status=status.HTTP_200_OK)

         except Exception :
             return Response({},status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None, *args, **kwargs):

        try:

            id = request.GET['business_id']
            business=Business.objects.get(pk=id)
            business_data=BusinessSerializer(business).data
            return Response(business_data, status= status.HTTP_200_OK)

        except Exception:
            return Response({}, status= status.HTTP_400_BAD_REQUEST)


    def patch(self, request, format=None, *args, **kwargs):
        pass
