# Generated by Django 4.2.3 on 2023-07-20 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_habit_is_completed_today_alter_habit_completed_times_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]