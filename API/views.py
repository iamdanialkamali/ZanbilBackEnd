# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser



from .models import Review,Services
import json
from .Token import Tokenizer as tokenizer
class TEST(APIView):
    parser_classes = (MultiPartParser,)
