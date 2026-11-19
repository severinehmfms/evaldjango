from django.urls import path

from . import views

app_name = "entraide"

urlpatterns = [
    # Vue pour la page d'accueil
    path("", views.index, name="index"),
    # Vue qui affiche toutes les compétences
    path("allskills/", views.SkillsView.as_view(), name="allskills"),
    # Première vue de mise à jour des compétences, avec des cases à cocher
    path("majskills/", views.majskills_view, name="majskills"),
    # Seconde vue de mise à jour des compétences, en utilisant ModelForm et liste déroulante
    path("majskillsbis/", views.majskillsbis_view, name="majskillsbis"),
    # Vue pour l'action de supprimer une compétence de l'utilisateur
    path("<int:skill_id>/supskilluser/", views.supskilluser_view, name="supskilluser"),
    # Vue pour ajouter un créneau
    path("addschedule/", views.addschedule_view, name="addschedule"),
    # Vue pour la page des créneaux qui n'ont encore trouvé aucune aide
    path("helpschedules/", views.helpschedules_view, name="helpschedules"),
    # Vue quand on souhaite aider quelqu'un
    path("<int:schedule_id>/help/", views.help_view, name="help"),
    # Vue pour se connecter
    path("login/", views.login_view, name="login"),
    # Vue pour se déconnecter
    path("logout/", views.logout_view, name="logout"),
]