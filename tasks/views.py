from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    if request.method == "POST":
        task_titles = request.POST.getlist("task[]")  # Get multiple tasks
        task_statuses = request.POST.getlist("status[]")  # Get multiple statuses

        for title, status in zip(task_titles, task_statuses):
            if title.strip():  # Prevent saving empty tasks
                Task.objects.create(title=title, status=status)

        return redirect("task_list")  # Refresh to display all tasks

    tasks = Task.objects.all()  # Fetch all tasks from database
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def remove_tasks(request):
    if request.method == "POST":
        Task.objects.all().delete()  # Deletes all tasks
        return redirect("task_list")
