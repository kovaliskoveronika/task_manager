from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Habit, User, TaskType, WeekTemplate
from .forms import (
    UserCreateForm,
    HabitCreateForm,
    TaskCreateForm,
    WeekTemplateForm,
    TaskWeekCreateForm,
    TaskTypeSearchNameForm,
    HabitSearchTitleForm,
    TaskSearchTitleForm,
)


@login_required
def index(request):
    """View function for the home page of the site."""
    num_completed_tasks = Task.objects.filter(completed=True, owner_id=request.user.id).count()
    num_habits = Habit.objects.filter(completed_times__gte=7, owner_id=request.user.id).count()

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
    paginate_by = 3

    def get_queryset(self):
        queryset = self.model.objects.filter(owner=self.request.user)
        form = HabitSearchTitleForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HabitsListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = HabitSearchTitleForm(initial={"title": title})
        return context


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
            habit.completed_times += 1
            habit.save()

        return redirect("manager:habit-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "manager/tasks_list.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = self.model.objects.filter(owner=self.request.user)
        form = TaskSearchTitleForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = TaskSearchTitleForm(initial={"title": title})
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:task-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskWeekCreateView(generic.FormView):
    template_name = "manager/task_form.html"
    form_class = TaskWeekCreateForm

    def get_success_url(self):
        return reverse("manager:week-template-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        week_template = get_object_or_404(WeekTemplate, id=self.kwargs["pk"])
        date = self.kwargs["day_number"]
        task = form.save(commit=False)
        task.date = week_template.get_day_by_number(date)
        task.owner = self.request.user
        task.save()
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


class TaskWeekDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task

    def get_success_url(self):
        return reverse("manager:week-template-detail", kwargs={"pk": self.kwargs["week_pk"]})


class TaskCompleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        if "complete" in request.POST:
            if not task.completed:
                task.completed = True
                task.save()
        week_template_id = request.POST.get("week_template_id")
        if week_template_id:
            return redirect("manager:week-template-detail", pk=week_template_id)
        return redirect("manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"
    paginate_by = 4

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchNameForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskTypeSearchNameForm(initial={"name": name})
        return context


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
    paginate_by = 4

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
        context = {
            "week_template": week_template,
        }
        return render(request, self.template_name, context)
