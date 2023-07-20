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
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    WeekTemplateListView,
    WeekTemplateCreateView,
    WeekTemplateDeleteView,
    WeekTemplateDetailView,
)

urlpatterns = [
    path("", index, name="home"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("habits/", HabitsListView.as_view(), name="habit-list"),
    path("habits/create/", HabitCreateView.as_view(), name="habit-create"),
    path("habits/<int:pk>/update/", HabitUpdateView.as_view(), name="habit-update"),
    path("habits/<int:pk>/delete/", HabitDeleteView.as_view(), name="habit-delete"),
    path("habits/<int:pk>/complete/", HabitCompleteView.as_view(), name="habit-complete"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/complete/", TaskCompleteView.as_view(), name="task-complete"),
    path("tasktypes/", TaskTypeListView.as_view(), name="task-type-list"),
    path("tasktypes/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("tasktypes/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("tasktypes/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("weektemplates/", WeekTemplateListView.as_view(), name="week-template-list"),
    path("weektemplates/create/", WeekTemplateCreateView.as_view(), name="week-template-create"),
    path("weektemplates/<int:pk>/delete/", WeekTemplateDeleteView.as_view(), name="week-template-delete"),
    path("weektemplates/<int:pk>/", WeekTemplateDetailView.as_view(), name="week-template-detail")
]

app_name = "manager"
