from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from manager.models import TaskType, WeekTemplate


class ModelsTest(TestCase):

    def test_user(self):
        test_user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
        )

        self.assertEquals(str(test_user), "test_user")

    def test_task_type(self):
        task_type = TaskType.objects.create(
            name="test_type"
        )

        self.assertEquals(str(task_type), "test_type")

    def test_week_str(self):
        test_user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
        )
        week = WeekTemplate.objects.create(
            start_date=timezone.datetime(2023, 7, 24).date(),
            owner=test_user
        )

        self.assertEquals(str(week), f"Week Template - starts {week.start_date}")

    def test_week_get_days(self):
        test_user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
        )
        week = WeekTemplate.objects.create(
            start_date=timezone.datetime(2023, 7, 24).date(),
            owner=test_user
        )

        days = week.get_days()

        self.assertEquals(len(days), 7)
        self.assertEquals(days[0]["date"], week.start_date)

    def test_week_get_day_by_number(self):
        test_user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
        )
        week = WeekTemplate.objects.create(
            start_date=timezone.datetime(2023, 7, 24).date(),
            owner=test_user
        )

        with self.assertRaises(ValueError):
            week.get_day_by_number(8)

        self.assertEquals(week.get_day_by_number(2), timezone.datetime(2023, 7, 25).date())
