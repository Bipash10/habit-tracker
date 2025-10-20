from django import forms
from .models import Habit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "description", "habit_type"]

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
