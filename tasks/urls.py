from django.urls import path
from .views import task_list, remove_tasks, edit_task

urlpatterns = [
    path("", task_list, name="task_list"),
    path("remove/", remove_tasks, name="remove_all_tasks"),
    path("edit/<int:task_id>/", edit_task, name="edit_task"),  # Task editing route
]
