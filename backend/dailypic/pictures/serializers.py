from pictures.models import Picture, Gallery, PictureOrder
from rest_framework import serializers

class PictureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Picture
        fields = ['id', 'thumbnail', 'url']

class PictureOrderSerializer(serializers.ModelSerializer):
    picture_id = serializers.ReadOnlyField(source='picture')

    class Meta:
        model = PictureOrder
        fields = ['id', 'query', 'picture_id', 'date']

class GallerySerializer(serializers.ModelSerializer):
    pictures = PictureOrderSerializer(required=False, many=True)

    class Meta:
        model = Gallery
        fields = ['id', 'title', 'pictures', 'owner']

class ImageRequestSerializer(serializers.Serializer):
    query = serializers.CharField()

    class Meta:
        fields = ['query']
