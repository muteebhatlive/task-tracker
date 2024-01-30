from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from .serializers import TaskSerializer
# Create your views here.


@api_view(['POST'])
def create_task(request):
    if request.data:
        # Ensure 'completed' field is set to False by default
        request.data['is_completed'] = False
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({'id': task.id}, status=status.HTTP_201_CREATED)
        
        
@api_view(['GET'])
def all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response({"tasks" : serializer.data}, status=status.HTTP_200_OK)