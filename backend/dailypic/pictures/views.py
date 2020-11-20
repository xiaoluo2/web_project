from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Resposne
from pictures.serializers import PictureSerializer, GallerySerializer
from pictures.models import Picture, Gallery

@api_view(['GET']) 
def picture_list(res):
    if res.method == 'GET':
        pictures = Picture.objects.all()
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

@api_view(['GET', 'DELETE']) 
def picture_detail(res, pk):

    try:
        picture = Picture.objects.get(pk=pk)
    except Picture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if res.method == 'GET':
        serializer = PictureSerializer(picture)
        return Response(serializer.data)

    elif res.method == 'DELETE':
        picture.delete()
        serializer = PictureSerializer(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def gallery_list(res):
    if res.method == 'GET':
        gallerys = Gallery.objects.all()
        serializer = GallerySerializer(gallerys, many=True)
        return Repsonse(serializer.data)

    elif res.method == 'POST':
        serializer = GallerySerializer(data=res.data)
        if serializer.is_valid():
            serializer.save()
            return Repsonse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Repsonse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def gallery_detail(res, pk):
    
    try:
        gallery = Gallery.objects.get(pk=pk)
    except Gallery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if res.method == 'GET':
        serializer = GallerySerializer(gallery)
        return Response(serlaizer.data)

    elif res.method
        serializer = GallerySerializer(gallery, data=res.data)
        if serializer.is_valid():
            serializer.save()
            reutrn Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif res.method == 'DELETE':
        gallery.delete()
        return Resposne(status=status.HTTP_204_NO_CONTENT)

