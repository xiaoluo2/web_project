from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Resposne
from django_celery_beat import PeriodicTask
from scheduler.serializers import PeriodicTaskSerializer 

@api_view(['GET', 'POST'])
def task_list(res, format=None):
    if res.method == 'GET':
        tasks = PeriodicTask.objects.all()
        serializer = PeriodicTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif res.method == 'POST':
        serializer = PeriodicTaskSerializer(data=res.data)
        if serializer.is_valid():
            serializer.save()
            return Repsonse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Repsonse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PUT', 'DELETE']) 
def task_detail(res, pk, format=None):

    try:
        task = PeriodicTask.objects.get(pk=pk)
    except PeriodicTask.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if res.method == 'GET':
        serializer = PeriodicTaskSerializer(task)
        return Response(serializer.data)

    elif res.method == 'PUT':
        serializer = PeriodicTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif res.method == 'DELETE':
        task.delete()
        serializer = PeriodicTaskSerializer(status=status.HTTP_204_NO_CONTENT)
