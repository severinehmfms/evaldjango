from django.urls import path

from . import views

app_name = "entraide"

urlpatterns = [
    path("", views.index, name="index"),
    path("allskills/", views.SkillsView.as_view(), name="allskills"),
    path("majskills/", views.majskills_view, name="majskills"),
    path("addschedule/", views.addschedule_view, name="addschedule"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]