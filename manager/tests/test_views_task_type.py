from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from manager.models import TaskType


class TaskTypePublicTest(TestCase):

    def test_task_type_list_public(self):
        res = self.client.get(reverse("manager:task-type-list"))

        self.assertNotEquals(res.status_code, 200)
        self.assertRedirects(res, "/accounts/login/?next=%2Ftasktypes%2F")


class TaskTypePrivateTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client = Client()
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(name="Work")

    def test_task_type_list(self):
        url = reverse("manager:task-type-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_type_list.html")
        self.assertIn(self.task_type, response.context["object_list"])

    def test_task_type_create(self):
        url = reverse("manager:task-type-create")
        data = {
            "name": "Personal",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskType.objects.count(), 2)
        self.assertTrue(TaskType.objects.filter(name="Personal").exists())

    def test_task_type_update(self):
        url = reverse("manager:task-type-update", args=[self.task_type.id])
        data = {
            "name": "Updated Type",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        updated_task_type = TaskType.objects.get(id=self.task_type.id)

        self.assertEqual(updated_task_type.name, "Updated Type")

    def test_task_type_delete(self):
        url = reverse("manager:task-type-delete", args=[self.task_type.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskType.objects.count(), 0)
