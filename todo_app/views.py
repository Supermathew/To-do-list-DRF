from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.throttling import UserRateThrottle
from django.shortcuts import get_object_or_404
from accounts.renderers import UserRenderer
from .models import TodoTask
from .serializers import TodoTaskSerializer

class TodoTaskListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    renderer_classes = [UserRenderer]

    def get(self, request):
        tasks = TodoTask.objects.filter(user=request.user)
        serializer = TodoTaskSerializer(tasks, many=True)
        return Response({
            'message': 'Tasks retrieved successfully',
            'tasks': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'message': 'Task created successfully',
                'task': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Invalid task data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TodoTaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    renderer_classes = [UserRenderer]

    def get_object(self, pk, user):
        return get_object_or_404(TodoTask, pk=pk, user=user)

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TodoTaskSerializer(task)
        return Response({
            'message': 'Task retrieved successfully',
            'task': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TodoTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Task updated successfully',
                'task': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Invalid task data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        task.delete()
        return Response({
            'message': 'Task deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class DeleteAllTasksView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    renderer_classes = [UserRenderer]

    def delete(self, request):
        TodoTask.objects.filter(user=request.user).delete()
        return Response({
            'message': 'All tasks deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)