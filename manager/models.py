from django.contrib.auth.models import AbstractUser
from django.db import models

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


class Priority(models.Model):
    name = models.CharField(max_length=150)
    difficulty = models.IntegerField()


class User(AbstractUser):
    pass


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=20,
                                choices=PRIORITY_CHOICES,
                                default="TO-DO")
    task_type = models.ForeignKey(to=TaskType, on_delete=models.CASCADE, related_name="tasks")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="tasks")


class Habit(models.Model):
    title = models.CharField(max_length=150)
    completed_times = models.IntegerField()
    repeatability = models.IntegerField()
    difficulty = models.CharField(max_length=20,
                                  choices=DIFFICULTY_CHOICES,
                                  default="TO-DO")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="tasks")
