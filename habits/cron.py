from .models import Habit, HabitRecord
from django.utils import timezone

def reset_habits_daily():
    today = timezone.now().date()
    for habit in Habit.objects.all():
        # Save pending habits as failed
        if habit.status_today == "pending":
            HabitRecord.objects.update_or_create(habit=habit, date=today, defaults={"status": "failed"})
        habit.status_today = "pending"
        habit.save()
