import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django import forms

from manager.forms import (
    UserCreateForm,
    HabitCreateForm,
    HabitSearchTitleForm,
    TaskCreateForm,
    TaskWeekCreateForm,
    TaskSearchTitleForm,
    TaskTypeSearchNameForm,
    WeekTemplateForm
)
from manager.models import Habit, Task, TaskType, WeekTemplate


class SearchFormsTest(TestCase):
    def test_habit_search_title(self):
        form = HabitSearchTitleForm()

        self.assertTrue(isinstance(form.fields["title"], forms.CharField))
        self.assertEquals(form.Meta.model, Habit)

    def test_task_search_title(self):
        form = TaskSearchTitleForm()

        self.assertTrue(isinstance(form.fields["title"], forms.CharField))
        self.assertEquals(form.Meta.model, Task)

    def test_task_type_search_name(self):
        form = TaskTypeSearchNameForm()

        self.assertTrue(isinstance(form.fields["name"], forms.CharField))


class UserCreateFormTests(TestCase):

    def test_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }

        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.first(), user)

    def test_password_not_match(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "test123",
        }

        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_no_username(self):
        form_data = {
            "password1": "testpassword123",
            "password2": "testpassword123",
        }

        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class HabitCreateFormTest(TestCase):
    def test_valid_form(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        form_data = {
            "title": "Test Habit",
            "repeatability": 5,
            "difficulty": "EASY",
        }

        form = HabitCreateForm(data=form_data)

        self.assertTrue(form.is_valid())

        habit = form.save(commit=False)
        habit.owner = user
        habit.save()

        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first(), habit)

    def test_invalid_repeatability(self):
        form_data = {
            "title": "Test Habit",
            "repeatability": 8,
            "difficulty": "EASY",
        }

        form = HabitCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_title(self):
        form_data = {
            "repeatability": 3,
            "difficulty": "EASY",
        }

        form = HabitCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TaskCreateFormTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.task_type = TaskType.objects.create(name="Test Task Type")

    def test_valid_form(self):
        form_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "date": datetime.date.today() + datetime.timedelta(days=1),
            "priority": "URGENT",
            "task_type": self.task_type.id,
        }

        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save(commit=False)
        task.owner = self.user
        task.save()

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first(), task)

    def test_past_date(self):
        form_data = {
            "title": "'Test Task",
            "description": "This is a test task",
            "date": datetime.date.today() - datetime.timedelta(days=1),
            "priority": "URGENT",
            "task_type": self.task_type.id,
        }

        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    def test_missing_task_type(self):
        form_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "date": datetime.date.today() + datetime.timedelta(days=1),
            "priority": "URGENT",
        }

        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("task_type", form.errors)


class TaskWeekCreateFormTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.task_type = TaskType.objects.create(
            name="Test Task Type"
        )
        self.week_template = WeekTemplate.objects.create(
            start_date=datetime.date.today(),
            owner=self.user
        )

    def test_valid_form(self):
        form_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "date": datetime.date.today() + datetime.timedelta(days=1),
            "priority": "URGENT",
            "task_type": self.task_type.id,
        }

        form = TaskWeekCreateForm(data=form_data)

        self.assertTrue(form.is_valid())

        task = form.save(commit=False)
        task.owner = self.user
        task.date = self.week_template.get_day_by_number(1)

        task.save()

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first(), task)

    def test_missing_task_type(self):
        form_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "date": datetime.date.today() + datetime.timedelta(days=1),
            "priority": "URGENT",
        }

        form = TaskWeekCreateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("task_type", form.errors)
