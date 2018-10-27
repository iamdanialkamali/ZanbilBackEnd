from .models import Users
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import HttpResponse,render
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.status import *
from rest_framework import authentication, permissions

from .Token import Tokenizer
from django.core import serializers

tokenizer = Tokenizer()
class AuthentiationController(APIView):

    def get(self,request,*args,**kwargs):
        pass
    def post(self, request, format=None, *args, **kwargs):
        try:
            data = json.loads(request.body)

            username = data["username"]
            password = data['password']
            user = User.objects.get(username=username)
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
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            email = data['email']
#            print(data)
            if(True): ##TODO: DATAValidation

                user = User.objects.create_user(username,email,password)
                return Response(tokenizer.user_token_generator(user),status.HTTP_201_CREATED)

            else:

                return Response({}, status=status.HTTP_400_BAD_REQUEST)##TODO:Serializer

        except Exception:
            return Response({}, status=status.HTTP_409_CONFLICT)##TODO:Serializer
