from django.urls import path
from .views import (
    TodoTaskListCreateView, 
    TodoTaskDetailView, 
    DeleteAllTasksView
)

urlpatterns = [
    path('tasks/', TodoTaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TodoTaskDetailView.as_view(), name='task-detail'),
    path('tasks/delete-all/', DeleteAllTasksView.as_view(), name='delete-all-tasks'),
]