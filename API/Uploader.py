from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from .Token import Tokenizer as tokenizer
from  .models import Picture
class ImageUploader(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None, *args, **kwargs):
        user_id = tokenizer.meta_decode(request.META)
        for_service = int(request.POST['for_service'])

        picture = request.FILES['picture']

        if(for_service):
            service_id = request.POST['service_id']
            pic = Picture.objects.create(service_id=service_id)

        else:
            business_id = request.POST['business_id']
            pic = Picture.objects.create(business_id=business_id)

        file = open("uploads/" + str(pic.id), 'wb')

        for byte in picture:
            file.write(bytearray(byte))
        file.close()
        return Response({}, status=status.HTTP_200_OK)
