from django.contrib.auth.models import User
from django.db import models

class Skill(models.Model):
    name_skill = models.CharField(max_length=200)

class User_Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Schedule(models.Model):
    # status ?
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)  # Si je supprime la compétence ça supprimera les schedules associés
    name_activity = models.CharField(max_length=200)
    date_help = models.DateTimeField("Créneau")

    # Si je supprime l'utilisateur ça supprimera les schedules associés
    # Obligée de rajouter related_name car sinon ça plante comme j'ai DEUX users en clé étrangère
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_schedules' )
    # user_creator_first_name = models.CharField(max_length=200)
    # user_creator_last_name = models.CharField(max_length=200)
    # user_creator_email = models.CharField(max_length=200)

    # Si je supprime l'utilisateur ça supprimera les schedules associés
    # Obligée de rajouter related_name car sinon ça plante comme j'ai DEUX users en clé étrangère
    user_helper = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='helped_schedules' )
    #user_helper_username = models.CharField(max_length=200)