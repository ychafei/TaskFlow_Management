from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def task_list(request):
    """Handles displaying tasks, adding new tasks, and filtering."""

    if request.method == "POST":
        task_titles = request.POST.getlist("task[]")
        task_statuses = request.POST.getlist("status[]")
        task_dates = request.POST.getlist("due_date[]")  # New line to capture due dates

        for title, status, due_date in zip(task_titles, task_statuses, task_dates):
            if title.strip():
                Task.objects.create(
                    title=title,
                    status=status,
                    due_date=due_date if due_date else None,
                    user=request.user
                )

        return redirect("task_list")

    filter_status = request.GET.get("filter_status")

    if filter_status and filter_status != "all":
        tasks = Task.objects.filter(user=request.user, status=filter_status)
    else:
        tasks = Task.objects.filter(user=request.user)

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "filter_status": filter_status
    })

@login_required
def remove_tasks(request):
    """Removes all tasks for the logged-in user."""
    if request.method == "POST":
        Task.objects.filter(user=request.user).delete()
        return redirect("task_list")

@login_required
def edit_task(request, task_id):
    """Handles editing an existing task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        new_title = request.POST.get("title")
        new_status = request.POST.get("status")
        new_due_date = request.POST.get("due_date")  # Capture updated due date

        if new_title.strip():
            task.title = new_title
            task.status = new_status
            task.due_date = new_due_date if new_due_date else None
            task.save()
            return redirect("task_list")

    return render(request, "tasks/edit_task.html", {"task": task})
