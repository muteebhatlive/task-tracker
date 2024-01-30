from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


# @api_view(['POST'])
# def create_task(request):
#     if request.data:
#         # Ensure 'completed' field is set to False by default
#         request.data['is_completed'] = False
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             task = serializer.save()
#             return Response({'id': task.id}, status=status.HTTP_201_CREATED)

class TaskAdd(APIView):
    def post(self, request):
        if 'tasks' in request.data:
            tasks_data = request.data['tasks']
            added_tasks = []

            for task_data in tasks_data:
                task_data['is_completed'] = task_data.get('is_completed', False)
                serializer = TaskSerializer(data=task_data)
                if serializer.is_valid():
                    task = serializer.save()
                    added_tasks.append({'id': task.id})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'tasks': added_tasks}, status=status.HTTP_201_CREATED)
        elif 'title' in request.data:
            request.data['is_completed'] = False
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                task = serializer.save()
                return Response({'id': task.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No tasks provided in request'}, status=status.HTTP_400_BAD_REQUEST)
    
    
   
    
    def delete(self, request):
        if 'tasks' in request.data:
            tasks_data = request.data['tasks']
            task_ids = []
            for task in tasks_data:
                if 'id' in task:
                    task_ids.append(task['id'])
                else:
                    return Response({'error': 'Task ID missing'}, status=status.HTTP_400_BAD_REQUEST)
            for id in task_ids:
                task_obj = Task.objects.filter(id=id)
                task_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'No tasks provided in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET'])
def all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response({"tasks" : serializer.data}, status=status.HTTP_200_OK)



class TaskDetail(APIView):
    def get_object(self, id):
        try:
            return Task.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def get(self, request, id):
        task = self.get_object(id)
        if not task:
            return Response({"error": "Task with id {} does not exist".format(id)}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        task = self.get_object(id)
        if not task:
            return Response({"error": "Task with id {} does not exist".format(id)}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
   

    def put(self, request, id):
        task = self.get_object(id)
        if not task:
            return Response({"error": "Task with id {} does not exist".format(id)}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)