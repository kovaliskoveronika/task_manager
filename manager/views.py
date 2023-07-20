from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Habit, User, TaskType, WeekTemplate
from .forms import UserCreateForm, HabitCreateForm, TaskCreateForm, WeekTemplateForm


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


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task-type-list")


class WeekTemplateListView(LoginRequiredMixin, generic.ListView):
    model = WeekTemplate
    template_name = "manager/week_template_list.html"

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class WeekTemplateCreateView(LoginRequiredMixin, generic.CreateView):
    model = WeekTemplate
    form_class = WeekTemplateForm
    template_name = "manager/week_template_form.html"
    success_url = reverse_lazy("manager:week-template-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WeekTemplateDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = WeekTemplate
    success_url = reverse_lazy("manager:week-template-list")


class WeekTemplateDetailView(View):
    template_name = "manager/week_template_detail.html"

    def get(self, request, *args, **kwargs):
        week_template = get_object_or_404(WeekTemplate, id=self.kwargs["pk"])
        days = self.get_days(week_template)
        context = {
            'week_template': week_template,
            'days': days,
        }
        return render(request, self.template_name, context)

    @staticmethod
    def get_days(week_template):
        days = []
        current_date = week_template.start_date
        for i in range(7):
            day_data = {
                'date': current_date,
                'day_name': current_date.strftime('%A'),
                'tasks': Task.objects.filter(date=current_date),
            }
            days.append(day_data)
            current_date += timezone.timedelta(days=1)
        return days
