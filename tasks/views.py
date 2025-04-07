from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db import connection
from datetime import datetime
from .models import Task
from .forms import TaskForm

def task_list(request):
    if not request.user.is_authenticated:
        return render(request, "tasks/guest_home.html")

    if request.method == "POST":
        task_titles = request.POST.getlist("task[]")
        statuses = request.POST.getlist("status[]")
        due_dates = request.POST.getlist("due_date[]")
        for title, status, due_date in zip(task_titles, statuses, due_dates):
            due_date_obj = None
            if due_date:
                try:
                    due_date_obj = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
                except ValueError:
                    due_date_obj = None
            Task.objects.create(user=request.user, title=title, status=status, due_date=due_date_obj)
        return redirect("task_list")

    filter_status = request.GET.get("filter_status", "all")
    tasks = Task.objects.filter(user=request.user)
    if filter_status != "all":
        tasks = tasks.filter(status=filter_status)

    tasks = tasks.order_by("due_date")

    today = timezone.now().date()
    enhanced_tasks = []
    for task in tasks:
        days_left = None
        overdue = False
        abs_days_left = None
        if task.due_date:
            delta = (task.due_date.date() - today).days
            days_left = delta
            overdue = delta < 0
            abs_days_left = abs(delta)
        enhanced_tasks.append({
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "due_date": task.due_date,
            "days_left": days_left,
            "overdue": overdue,
            "abs_days_left": abs_days_left,
        })

    return render(request, "tasks/task_list.html", {
        "tasks": enhanced_tasks,
        "filter_status": filter_status,
    })

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/edit_task.html", {"form": form, "task": task})

@login_required
def update_task_status(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        statuses = ["not_completed", "in_progress", "completed"]
        try:
            current_index = statuses.index(task.status)
            next_status = statuses[(current_index + 1) % len(statuses)]
        except ValueError:
            next_status = "not_completed"
        task.status = next_status
        task.save()
        return JsonResponse({"success": True, "new_status": next_status})
    return JsonResponse({"success": False})

@login_required
def remove_all_tasks(request):
    if request.method == "POST":
        Task.objects.filter(user=request.user).delete()
    return redirect("task_list")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
    return redirect("task_list")

@login_required
def create_task_sql(request):
    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status", "not_completed")
        due_date = request.POST.get("due_date") or None

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tasks_task (title, status, due_date, user_id)
                VALUES (%s, %s, %s, %s)
            """, [title, status, due_date, request.user.id])
        return redirect("list_tasks_sql")

    return render(request, "tasks/create_sql.html")

@login_required
def list_tasks_sql(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, status, due_date FROM tasks_task WHERE user_id = %s", [request.user.id])
        task_rows = cursor.fetchall()

    tasks = []
    for row in task_rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "status": row[2],
            "due_date": row[3],
        })

    return render(request, "tasks/list_sql.html", {"tasks": tasks})

@login_required
def edit_task_sql(request, task_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, status, due_date FROM tasks_task WHERE id = %s AND user_id = %s", [task_id, request.user.id])
        row = cursor.fetchone()

    if not row:
        return redirect("list_tasks_sql")

    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status", "not_completed")
        due_date = request.POST.get("due_date") or None

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE tasks_task SET title = %s, status = %s, due_date = %s
                WHERE id = %s AND user_id = %s
            """, [title, status, due_date, task_id, request.user.id])
        return redirect("list_tasks_sql")

    task = {
        "id": row[0],
        "title": row[1],
        "status": row[2],
        "due_date": row[3].strftime("%Y-%m-%dT%H:%M") if row[3] else "",
    }
    return render(request, "tasks/edit_sql.html", {"task": task})

@login_required
def delete_task_sql(request, task_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tasks_task WHERE id = %s AND user_id = %s", [task_id, request.user.id])
    return redirect("list_tasks_sql")
