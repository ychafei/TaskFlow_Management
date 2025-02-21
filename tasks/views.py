from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    if request.method == "POST":
        task_title = request.POST.get("task")
        task_status = request.POST.get("status")
        if task_title:  # Ensure at least one task is entered
            Task.objects.create(title=task_title, status=task_status)
        return redirect("task_list")  # Refresh page to show updated tasks

    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def remove_tasks(request):
    if request.method == "POST":
        Task.objects.all().delete()  # Deletes all tasks
    return redirect("task_list")  # Redirect even if accessed via GET
