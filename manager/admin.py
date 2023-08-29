from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from manager.models import TaskType, User, Task, Habit

admin.site.register(TaskType)
admin.site.register(Task)
admin.site.register(Habit)

admin.site.register(User, UserAdmin)
