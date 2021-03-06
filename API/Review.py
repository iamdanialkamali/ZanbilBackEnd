
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import ReviewSerializer

from .models import Review,Services
import json
from .Token import Tokenizer as tokenizer
class ReviewController(APIView):
    def put(self, request, format=None, *args, **kwargs):
         try:
            user_id = tokenizer.meta_decode(request.META)
            data = json.loads(request.body)
            point = float(data['point'])
            description = data['description']
            service_id = data['service_id']

            if 0 <= point <= 10 :
                self.newPointCalculator(service_id,point)
                my_review = Review.objects.create(
                    user_id=user_id,
                    description=description,
                    service_id=service_id,
                    rating=point
                )
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            return Response({}, status=status.HTTP_200_OK)

         except Exception :
             return Response({}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None, *args, **kwargs):

        # try:
            id = request.GET['business_id']
            reviews = Review.objects.filter(service__business__id=id)

            review_datas = ReviewSerializer(reviews,many=True).data
            return Response(review_datas, status= status.HTTP_200_OK)

        # except Exception:
        #     return Response({}, status= status.HTTP_400_BAD_REQUEST)
    @staticmethod
    def newPointCalculator(service_id,point):
        service = Services.objects.get(pk=service_id)
        service.rating = (service.rating*service.review_count + point)/(service.review_count+1)
        service.review_count = service.review_count + 1
        service.save(force_update=True)
