from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


"""
* Modèle Skill (compétence)
"""
class Skill(models.Model):
    name_skill = models.CharField(max_length=200)

    def __str__(self):
        return self.name_skill


"""
* Modèle UserSkill représente une compétence associée à un utilisateur
"""
class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


"""
* Représente un créneau pour une activité donnée.
* Dans le futur, on pourra modifier et au lieu d'avoir juste une date d'avoir une heure de départ et heure de fin
* On pourra également avoir une activité à vide pour différencier un créneau pour une activité donnée, d'un créneau disponible pour aider les autres
"""

class Schedule(models.Model):
    # status ?
    # Si je supprime la compétence ça supprimera les schedules associés
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    name_activity = models.CharField(max_length=200)
    date_help = models.DateTimeField("Créneau")

    # Si je supprime l'utilisateur ça supprimera les schedules associés
    # Obligée de rajouter related_name car sinon ça plante comme j'ai DEUX users en clé étrangère
    # (en fait django crée un nom inverse et comme j'ai DEUX users à l'inverse dans user on se retrouve avec deux fois le même nom)
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_schedules' )
    # user_creator_first_name = models.CharField(max_length=200)
    # user_creator_last_name = models.CharField(max_length=200)
    # user_creator_email = models.CharField(max_length=200)

    # Si je supprime l'utilisateur ça supprimera les schedules associés
    # Obligée de rajouter related_name car sinon ça plante comme j'ai DEUX users en clé étrangère
    user_helper = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='helped_schedules' )
    #user_helper_username = models.CharField(max_length=200)

    def __str__(self):
        date_locale = timezone.localtime(self.date_help)
        return self.name_activity+ " - " + date_locale.strftime("%d/%m/%Y à %Hh%M")
