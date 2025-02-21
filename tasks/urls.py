from django.urls import path
from .views import task_list, remove_tasks

urlpatterns = [
    path("", task_list, name="task_list"),
    path("remove/", remove_tasks, name="remove_all_tasks"),
]
