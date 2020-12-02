from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import UserRateThrottle

from pictures.serializers import PictureSerializer, GallerySerializer, ImageRequestSerializer
from pictures.models import Picture, Gallery
from pictures.tasks import pull_image
from pictures.permissons import IsOwner, IsAdminOrReadOnly

import json

# make request and reutrn image urls
@api_view(['POST'])
@permission_classes([AllowAny])
def pull_request(response):
    print(response.META)
    print(response.data);
    serializer = ImageRequestSerializer(data=response.data)

    serializer.is_valid(raise_exception=True)
    data = serializer.data
    r = pull_image(data['query'])
    id = r.get()
    try:
        pic = Picture.objects.get(pk=id)
    except Picture.DoesNotExist:
        pic = None
    if pic is not None:
        urls = {'url': pic.url, 'thumbnail': pic.thumbnail}

    pic_data = json.dumps(urls)
    return Response(pic_data)

class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [IsAdminOrReadOnly]

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsOwner | IsAdminUser]
