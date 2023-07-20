from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

PRIORITY_CHOICES = (
    ("TO-DO", "TO-DO"),
    ("URGENT", "URGENT"),
    ("OPTIONAL", "OPTIONAL"),
)

DIFFICULTY_CHOICES = (
    ("EASY", "EASY"),
    ("CAN BE", "CAN BE"),
    ("HARD WORK", "HARD WORK"),
)


class TaskType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class User(AbstractUser):

    def __str__(self):
        return self.username


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=20,
                                choices=PRIORITY_CHOICES,
                                default="TO-DO",
                                null=True
                                )
    task_type = models.ForeignKey(to=TaskType, on_delete=models.CASCADE, related_name="tasks")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="tasks")


class Habit(models.Model):
    title = models.CharField(max_length=150)
    completed_times = models.IntegerField(default=0)
    is_completed_today = models.BooleanField(default=False)
    repeatability = models.IntegerField(default=7)
    difficulty = models.CharField(max_length=20,
                                  choices=DIFFICULTY_CHOICES,
                                  default="CAN BE",
                                  null=True
                                  )
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="habits")


class WeekTemplate(models.Model):
    start_date = models.DateField(default=timezone.now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="week_templates")

    def __str__(self):
        return f"starts {self.start_date}"
