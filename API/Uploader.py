from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from .Token import Tokenizer as tokenizer
class UploadController(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None, *args, **kwargs):
        user_id = tokenizer.meta_decode(request.META)
        for_service = request.POST['for_service']
        if(for_service):
            ali = request.FILES['picture']
            file = open("uploads/"+ali.name,'wb')
            for i in ali:
                file.write(bytearray(i))
            file.close()

            return Response({}, status=status.HTTP_200_OK)
