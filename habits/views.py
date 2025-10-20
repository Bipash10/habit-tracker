from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import HabitForm, SignUpForm
from .models import Habit

# ----------------- Authentication -----------------

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "habits/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "habits/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


# ----------------- Habit Views -----------------

@login_required
def home(request):
    good_habits = Habit.objects.filter(user=request.user, habit_type="good")
    bad_habits = Habit.objects.filter(user=request.user, habit_type="bad")
    return render(request, "habits/home.html", {"good_habits": good_habits, "bad_habits": bad_habits})

@login_required
def add_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("home")
    else:
        form = HabitForm()
    return render(request, "habits/add_habit.html", {"form": form})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect("home")

@login_required
def mark_done(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.status_today = "completed"
    habit.total_completed += 1
    habit.save()
    return redirect("home")

@login_required
def mark_failed(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.status_today = "failed"
    habit.total_failed += 1
    habit.save()
    return redirect("home")


@login_required
def analytics(request):
    habits = Habit.objects.filter(user=request.user)

    total_habits = habits.count()
    total_completed = sum(habit.total_completed for habit in habits)
    total_failed = sum(habit.total_failed for habit in habits)
    overall_completion_rate = round(
        (total_completed / (total_completed + total_failed) * 100) if (total_completed + total_failed) > 0 else 0, 2
    )

    # Compute per-habit completion rates
    habit_stats = []
    for habit in habits:
        total = habit.total_completed + habit.total_failed
        rate = round((habit.total_completed / total * 100), 2) if total > 0 else 0
        habit_stats.append({
            "name": habit.name,
            "type": habit.habit_type,
            "completed": habit.total_completed,
            "failed": habit.total_failed,
            "completion_rate": rate,
        })

    context = {
        "total_habits": total_habits,
        "total_completed": total_completed,
        "total_failed": total_failed,
        "overall_completion_rate": overall_completion_rate,
        "habit_stats": habit_stats,
    }

    return render(request, "habits/analytics.html", context)
