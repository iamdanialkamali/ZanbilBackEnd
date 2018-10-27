from rest_framework import serializers

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
