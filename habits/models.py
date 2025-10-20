from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    HABIT_TYPE_CHOICES = [
        ("good", "Good"),
        ("bad", "Bad"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    habit_type = models.CharField(max_length=10, choices=HABIT_TYPE_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    status_today = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    total_completed = models.PositiveIntegerField(default=0)
    total_failed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_completion_rate(self):
        total = self.total_completed + self.total_failed
        return round((self.total_completed / total) * 100, 2) if total > 0 else 0
