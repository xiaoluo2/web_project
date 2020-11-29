from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView

from pictures.serializers import PictureSerializer, GallerySerializer, ImageRequestSerializer
from pictures.models import Picture, Gallery
from pictures.tasks import pull_image
from pictures.permissons import IsOwner

from celery.result import AsyncResult
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def pull_request(response):
    serializer = ImageRequestSerializer(data=response.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    
    task_list = [pull_image.delay(data['query']) for i in range(data['number'])]
    res_list = [r.get() for r in task_list]
    pic_list = [AsyncResult(id).get() for id in res_list]
    pic_data = json.dumps({"pictures": pic_list})
    return Response(pic_data)

class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsOwner | IsAdminUser]
