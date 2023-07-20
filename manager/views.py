from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from manager.models import Task, Habit


@login_required
def index(request):
    """View function for the home page of the site."""
    num_completed_tasks = Task.objects.filter(completed=True).count()
    num_habits = Habit.objects.filter(completed_times__gte=7).count()

    context = {
        "num_tasks": num_completed_tasks,
        "num_habits": num_habits
    }

    return render(request, "manager/home.html", context=context)
