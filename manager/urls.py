from django.urls import path

from .views import (
    index,
    UserCreateView,
    HabitsListView,
    HabitCreateView,
    HabitUpdateView,
    HabitDeleteView,
    HabitCompleteView
)

urlpatterns = [
    path("", index, name="home"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("habits/", HabitsListView.as_view(), name="habit-list"),
    path("habits/create/", HabitCreateView.as_view(), name="habit-create"),
    path("habits/<int:pk>/update", HabitUpdateView.as_view(), name="habit-update"),
    path("habits/<int:pk>/delete", HabitDeleteView.as_view(), name="habit-delete"),
    path("habits/<int:pk>/complete/", HabitCompleteView.as_view(), name="habit-complete"),
]

app_name = "manager"
