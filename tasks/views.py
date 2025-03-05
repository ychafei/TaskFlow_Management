from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def task_list(request):
    """Handles displaying tasks, adding new tasks, and filtering."""
    
    if request.method == "POST":
        task_titles = request.POST.getlist("task[]")  # Get multiple tasks
        task_statuses = request.POST.getlist("status[]")  # Get multiple statuses

        for title, status in zip(task_titles, task_statuses):
            if title.strip():  # Prevent saving empty tasks
                Task.objects.create(title=title, status=status)

        return redirect("task_list")  # Refresh page to display all tasks

    # Filtering 
    filter_status = request.GET.get("filter_status")  # Get filter value from URL params
    if filter_status and filter_status != "all":
        tasks = Task.objects.filter(status=filter_status)
    else:
        tasks = Task.objects.all()  # Show all tasks if no filter is applied

    return render(request, "tasks/task_list.html", {"tasks": tasks, "filter_status": filter_status})


def remove_tasks(request):
    """Handles removing all tasks."""
    if request.method == "POST":
        Task.objects.all().delete()  # Deletes all tasks
        return redirect("task_list")


def edit_task(request, task_id):
    """Handles editing an existing task."""
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        new_title = request.POST.get("title")
        new_status = request.POST.get("status")

        if new_title.strip():  # Ensure the title is not empty
            task.title = new_title
            task.status = new_status
            task.save()
            return redirect("task_list")  # Redirect after editing

    return render(request, "tasks/edit_task.html", {"task": task})
