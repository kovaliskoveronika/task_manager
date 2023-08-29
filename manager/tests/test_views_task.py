from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from manager.models import Task, TaskType


class TaskPublicTest(TestCase):
    def test_task_list_public(self):
        res = self.client.get(reverse("manager:task-list"))

        self.assertNotEquals(res.status_code, 200)
        self.assertRedirects(res, "/accounts/login/?next=%2Ftasks%2F")


class TaskPrivateTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client = Client()
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(
            name="personal"
        )

        self.task = Task.objects.create(
            title="Test Task",
            owner=self.user,
            description="This is a test task description.",
            priority="URGENT",
            task_type=self.task_type
        )

    def test_task_list(self):
        url = reverse("manager:task-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/tasks_list.html")
        self.assertIn(self.task, response.context["object_list"])

    def test_task_create(self):
        url = reverse("manager:task-create")
        data = {
            "title": "New Task",
            "description": "This is a new task description.",
            "date": timezone.datetime(2023, 7, 24).date(),
            "priority": "TO-DO",
            "task_type": self.task_type.id,
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

        new_task = Task.objects.get(title="New Task")
        self.assertEqual(new_task.owner, self.user)

    def test_task_update(self):
        url = reverse("manager:task-update", args=[self.task.id])
        data = {
            "title": "Updated Task",
            "description": "This is an updated task description.",
            "date": timezone.datetime(2023, 7, 24).date(),
            "priority": "TO-DO",
            "task_type": self.task_type.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        updated_task = Task.objects.get(id=self.task.id)

        self.assertEqual(updated_task.title, "Updated Task")

    def test_task_delete(self):
        url = reverse("manager:task-delete", args=[self.task.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_complete(self):
        url = reverse("manager:task-complete", args=[self.task.id])
        data = {"complete": "true"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()

        self.assertTrue(self.task.completed)
