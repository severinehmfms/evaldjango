from django.urls import path

from . import views

app_name = "entraide"

urlpatterns = [
    path("", views.index, name="index"),
    path("allskills/", views.SkillsView.as_view(), name="allskills"),
    path("majskills/", views.majskills_view, name="majskills"),
    path("majskillsbis/", views.majskillsbis_view, name="majskillsbis"),    # Deuxième formulaire pour les compétences
    path("addschedule/", views.addschedule_view, name="addschedule"),
    path("helpschedules/", views.helpschedules_view, name="helpschedules"),
    path("<int:schedule_id>/help/", views.help_view, name="help"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]