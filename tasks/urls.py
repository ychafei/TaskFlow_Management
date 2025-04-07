# tasks/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),
    
    # ✅ MUST match the AJAX fetch path in task_list.html
    path("<int:task_id>/update_status/", views.update_task_status, name="update_task_status"),

    path("remove_all/", views.remove_all_tasks, name="remove_all_tasks"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),

    # ✅ Raw SQL CRUD routes
    path("sql/create/", views.create_task_sql, name="create_task_sql"),
    path("sql/tasks/", views.list_tasks_sql, name="list_tasks_sql"),
    path("sql/edit/<int:task_id>/", views.edit_task_sql, name="edit_task_sql"),
    path("sql/delete/<int:task_id>/", views.delete_task_sql, name="delete_task_sql"),
]
