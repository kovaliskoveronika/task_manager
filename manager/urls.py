from django.urls import path

from .views import (
    index,
    UserCreateView,
    HabitsListView,
    HabitCreateView,
    HabitUpdateView,
    HabitDeleteView,
    HabitCompleteView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskCompleteView,
)

urlpatterns = [
    path("", index, name="home"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("habits/", HabitsListView.as_view(), name="habit-list"),
    path("habits/create/", HabitCreateView.as_view(), name="habit-create"),
    path("habits/<int:pk>/update", HabitUpdateView.as_view(), name="habit-update"),
    path("habits/<int:pk>/delete", HabitDeleteView.as_view(), name="habit-delete"),
    path("habits/<int:pk>/complete/", HabitCompleteView.as_view(), name="habit-complete"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/complete/", TaskCompleteView.as_view(), name="task-complete"),
]

app_name = "manager"
