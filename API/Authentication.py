from django.contrib.auth.models import User
from .models import Users

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .Token import Tokenizer

tokenizer = Tokenizer()
class AuthentiationController(APIView):

    def get(self,request,*args,**kwargs):
        pass
    def post(self, request, format=None, *args, **kwargs):
        try:
            data = json.loads(request.body)

            username = data["username"]
            password = data['password']

            user = Users.objects.get(username=username)
            is_user = user.check_password(raw_password=password)

            if(is_user):
                message = {
                        'id': user.id
                }
                return Response({
                    'jwt': tokenizer.endcode(message)
                },
                    status=status.HTTP_200_OK)
            return Response('NOT FOUND', status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception :
            return Response('NOT FOUND',status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None, *args, **kwargs):
        # try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            email = data['email']
            phone_number = data["phone_number"]
#            print(data)
            if(True): ##TODO: DATAValidation

                user = Users.objects.create_user(username,email,password,phone_number=phone_number)
                return Response(tokenizer.user_token_generator(user),status.HTTP_201_CREATED)

            else:

                return Response({}, status=status.HTTP_400_BAD_REQUEST)##TODO:Serializer

        # except Exception:
        #     return Response({}, status=status.HTTP_409_CONFLICT)##TODO:Serializer
