from django.urls import path
from .views import *



urlpatterns = [
    path('tasks',create_task, name='task_create'),
    path('tasks/all', all_tasks, name='all_tasks'),
    path('tasks/<int:id>', TaskDetail.as_view(), name='task_detail'),

    # other endpoints...
]