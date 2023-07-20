import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User, Habit, Task, WeekTemplate


class UserCreateForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
        )


class HabitCreateForm(forms.ModelForm):

    class Meta:
        model = Habit
        fields = ["title", "repeatability", "difficulty"]

    def clean_repeatability(self):
        repeatability = self.cleaned_data["repeatability"]

        if repeatability > 7:
            raise ValidationError("Habits repeatability must be less or equal 7")
        return repeatability


class TaskCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title", "description", "date", "priority", "task_type"]
        widgets = {
            "date": forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date(self):
        date = self.cleaned_data["date"]

        if date.date() < datetime.date.today():
            raise ValidationError("You can not plan past(")
        return date


class WeekTemplateForm(forms.ModelForm):
    class Meta:
        model = WeekTemplate
        fields = ["start_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]

        if start_date.weekday() != 0:
            raise ValidationError("Week must start on monday")
        if start_date < datetime.date.today():
            raise ValidationError("You can not plan past(")
        return start_date
