from django.urls import path
from .views import task_list, remove_tasks  # Import remove_tasks

urlpatterns = [
    path("", task_list, name="task_list"),
    path("remove_all/", remove_tasks, name="remove_tasks"),  # Use "remove_tasks" as the name
]
