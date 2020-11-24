from pictures.models import Picture, Gallery
from rest_framework import serializers

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'hashvalue', 'url']

class GallerySerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(required=False, many=True)

    class Meta:
        model = Gallery
        fields = ['id', 'title', 'pictures', 'user']
