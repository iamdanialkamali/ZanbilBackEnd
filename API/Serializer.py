from rest_framework import serializers
from .models import Business, Services, TimeTable, Sans, Categories, Review, Users, Reserves, Picture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = [
            'id',
        ]


class ServiceSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)

    class Meta:
        model = Services
        fields = [
            'id',
            'business',
            'name',
            'fee',
            'rating',
            'timetable',
            'description',
            'pictures',
        ]


class SansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sans
        fields = [
            'id',
            'start_time',
            'end_time',
            'timetable_id',
            'weekday',
        ]


class BusinessSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    pictures = PictureSerializer(many=True)

    class Meta:
        model = Business
        fields = [
            'id',
            'owner_id',
            'name',
            'phone_number',
            'email',
            'address',
            'services',
            'description',
            'category_id',
            'pictures',
        ]


class BusinessSimpleSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)
    class Meta:
        model = Business
        fields = [
            'id',
            'owner_id',
            'name',
            'phone_number',
            'email',
            'address',
            'description',
            'category_id',
            'pictures'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            'id',
            'name',
        ]


class TimetableSimpleSerializer(serializers.ModelSerializer):
    sanses = SansSerializer(many=True)

    class Meta:
        model = TimeTable
        fields = [
            'id',
            'name',
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'username',
            'email',
            'phone_number',
        ]

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'username',
        ]


class ReservesSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Reserves
        fields = [
            'date',
            'description',
            'service'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UsernameSerializer()

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'description',
            'rating',
        ]


class ServiceSearchSerializer(serializers.ModelSerializer):
    business = BusinessSimpleSerializer()
    pictures = PictureSerializer()
    class Meta:
        model = Services
        fields = [
            'id',
            'business',
            'name',
            'fee',
            'rating',
            'timetable',
            'description',
            'pictures',
        ]

# class BusinessSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Business
#         fields=[
#             'id',
#             'owner_id',
#             'name',
#             'phone_number',
#             'email',
#             'address',
#             'description',
#             'category_id'
#         ]
# class LoginSerializer(serializers.ModelSerializer):
#     tracks = serializers.HyperlinkedRelatedField(
#             many=True,
#             read_only=True,
#             view_name='track-detail'
#         )
#
#         class Meta:
#             model = Album
#             fields = ('album_name', 'artist', 'tracks')
# #    username = serializers.
#     username = serializers.CharField(max_length=200)
#     password = serializers.CharField(max_length=200)
