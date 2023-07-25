from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from manager.models import WeekTemplate


class WeekTemplatePublicTest(TestCase):
    def test_week_template_list_public(self):
        res = self.client.get(reverse("manager:week-template-list"))

        self.assertNotEquals(res.status_code, 200)
        self.assertRedirects(res, "/accounts/login/?next=%2Fweektemplates%2F")


class WeekTemplatePrivateTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

        self.week_template = WeekTemplate.objects.create(
            start_date=timezone.datetime(2023, 7, 24).date(),
            owner=self.user
        )

    def test_week_template_list(self):
        url = reverse("manager:week-template-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/week_template_list.html")
        self.assertIn(self.week_template, response.context["object_list"])

    def test_week_template_create(self):
        url = reverse("manager:week-template-create")
        data = {
            "start_date": timezone.datetime(2023, 7, 31).date(),
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(WeekTemplate.objects.count(), 2)

    def test_week_template_delete(self):
        url = reverse("manager:week-template-delete", args=[self.week_template.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(WeekTemplate.objects.count(), 0)

    def test_week_template_detail(self):
        url = reverse("manager:week-template-detail", args=[self.week_template.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/week_template_detail.html")
        self.assertEqual(response.context["week_template"], self.week_template)
