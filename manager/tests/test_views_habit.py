from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Habit


class HabitPublicTest(TestCase):

    def test_habit_list_public(self):
        res = self.client.get(reverse("manager:habit-list"))

        self.assertNotEquals(res.status_code, 200)
        self.assertRedirects(res, "/accounts/login/?next=%2Fhabits%2F")


class HabitPrivateTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.client.force_login(self.user)

    def test_habit_create(self):
        url = reverse("manager:habit-create")
        data = {
            "title": "test_title",
            "repeatability": 5,
            "difficulty": "EASY"
        }

        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)

        habit = Habit.objects.get(id=1)

        self.assertEqual(habit.title, "test_title")
        self.assertEqual(habit.repeatability, 5)
        self.assertEqual(habit.difficulty, "EASY")
        self.assertEqual(habit.owner.id, self.user.id)

    def test_habit_update(self):
        self.habit = Habit.objects.create(
            title="Old Title",
            repeatability=3,
            difficulty="MEDIUM",
            owner=self.user,
        )
        url = reverse("manager:habit-update", kwargs={"pk": self.habit.id})
        data = {
            "title": "New Title",
            "repeatability": 5,
            "difficulty": "EASY",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.title, "New Title")
        self.assertEqual(self.habit.repeatability, 5)
        self.assertEqual(self.habit.difficulty, "EASY")

    def test_habit_delete(self):
        habit = Habit.objects.create(
            title="Test Habit",
            repeatability=3,
            difficulty="MEDIUM",
            owner=self.user,
            completed_times=0,
        )
        self.client.login(username='testuser', password='testpassword')
        url = reverse("manager:habit-delete", kwargs={"pk": habit.id})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Habit.objects.filter(pk=habit.id).exists())

    def test_habit_complete(self):
        habit = Habit.objects.create(
            title="Test Habit",
            repeatability=3,
            difficulty="MEDIUM",
            owner=self.user,
            completed_times=0,
        )
        self.client.login(username='testuser', password='testpassword')
        url = reverse("manager:habit-complete", kwargs={"pk": habit.id})

        response = self.client.post(url, {"complete": True})

        self.assertEqual(response.status_code, 302)
        habit.refresh_from_db()
        self.assertEqual(habit.completed_times, 1)
