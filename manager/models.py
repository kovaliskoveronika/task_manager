from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from constants import PRIORITY_CHOICES, DIFFICULTY_CHOICES


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
        return f"Week Template - starts {self.start_date}"

    def get_days(self):
        days = []
        current_date = self.start_date
        for i in range(7):
            day_data = {
                "date": current_date,
                "day_name": current_date.strftime("%A"),
                "tasks": Task.objects.filter(date=current_date),
            }
            days.append(day_data)
            current_date += timezone.timedelta(days=1)
        return days

    def get_day_by_number(self, day_number):
        if day_number < 1 or day_number > 7:
            raise ValueError("Invalid day number")
        return self.start_date + timezone.timedelta(days=day_number - 1)
