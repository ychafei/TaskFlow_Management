from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status", "not_completed")  # Default to not completed
        if title:  # Ensure at least one task is added
            Task.objects.create(title=title, status=status)
        return redirect("task_list")

    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def remove_tasks(request):
    if request.method == "POST":
        Task.objects.filter(status__in=["not_completed", "in_progress"]).delete()
    return redirect("task_list")  # Redirect back to task list