from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Resposne
from rest_framework import viewsets

from pictures.serializers import PictureSerializer, GallerySerializer, ImageRequestSerializer
from pictures.models import Picture, Gallery
from pictures.tasks import pull_image
from pictures.permissons import IsOwnerOrIsAdmin

@api_view(['POST'])
@permission_classes(AllowAny)
def pull_request(response):
    serializer = ImageRequestSerializer(data=response.data)
    pictures = pull_images.delay(serializer.query, serializer.number).get()
    return Response(pictures)

class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsOwner | IsAdmin]
