from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Habit, User
from .forms import UserCreateForm, HabitCreateForm, TaskCreateForm


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


class UserCreateView(generic.CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "registration/registrate.html"
    success_url = reverse_lazy("manager:home")


class HabitsListView(LoginRequiredMixin, generic.ListView):
    model = Habit
    template_name = "manager/habits_list.html"

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class HabitCreateView(LoginRequiredMixin, generic.CreateView):
    model = Habit
    form_class = HabitCreateForm
    template_name = "manager/habit_form.html"
    success_url = reverse_lazy("manager:habit-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class HabitUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Habit
    form_class = HabitCreateForm
    template_name = "manager/habit_form.html"
    success_url = reverse_lazy("manager:habit-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class HabitDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Habit
    success_url = reverse_lazy("manager:habit-list")


class HabitCompleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk)

        if "complete" in request.POST:
            if not habit.is_completed_today:
                habit.completed_times += 1
                habit.is_completed_today = True
                habit.save()

        return redirect("manager:habit-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "manager/tasks_list.html"

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")


class TaskCompleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        if "complete" in request.POST:
            if not task.completed:
                task.completed = True
                task.save()

        return redirect("manager:task-list")
