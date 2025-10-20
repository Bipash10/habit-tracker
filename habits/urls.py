from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_habit, name="add_habit"),
    path("delete/<int:habit_id>/", views.delete_habit, name="delete_habit"),
    path("done/<int:habit_id>/", views.mark_done, name="mark_done"),
    path("fail/<int:habit_id>/", views.mark_failed, name="mark_failed"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("analytics/", views.analytics, name="analytics"),
    ]
