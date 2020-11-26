from pictures.models import Picture, Gallery
from rest_framework import serializers

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'hashvalue', 'url']

class PictureOrderSerializer(serializers.ModelSerializer):
    picture_url = serializers.ReadOnlyField(source='picture.url')

    class Meta:
        model = PictureOrder
        fields = ['id', 'query', 'picture_url', 'date']

class GallerySerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(source='pictures', required=False, many=True)

    class Meta:
        model = Gallery
        fields = ['id', 'title', 'pictures', 'user']

class ImageRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=50)
