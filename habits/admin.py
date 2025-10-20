from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'habit_type', 'status_today', 'total_completed', 'total_failed')
    list_filter = ('habit_type', 'status_today')
    search_fields = ('name',)
