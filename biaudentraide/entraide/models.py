from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Skill(models.Model):
    """
    * Modèle Skill (compétence)
    """
    name_skill = models.CharField(max_length=200)

    def __str__(self):
        return self.name_skill

    @classmethod
    def get_user_skills(cls, user):
        """Méthode qui va retourner toutes les Skills d'un utilisateur"""
        return Skill.objects.filter(userskill__user=user)


class UserSkill(models.Model):
    """
    * Modèle UserSkill représente une compétence associée à un utilisateur
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'skill'], name='unique_user_skill')]


class Schedule(models.Model):
    """
    * Modèle Schedule
    * Représente un créneau pour une activité donnée.
    * Plus tard, on pourra modifier et au lieu d'avoir juste une date, avoir une date/heure départ et date/heure fin
    * Plus tard, on gérera le name_activity à vide pour préciser qu'un créneau est disponible
    """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    name_activity = models.CharField(max_length=200)
    date_help = models.DateTimeField("Créneau")

    # Si je supprime l'utilisateur ça supprimera les schedules associés
    # Obligée de rajouter related_name car sinon ça plante comme j'ai DEUX users en clé étrangère
    # (Django crée une variable dans User, j'ai DEUX users donc il veut créer dans user deux fois le même nom)
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                     blank=True, related_name='created_schedules')

    # Si je supprime l'utilisateur ça supprimera les schedules associés
    # Obligée de rajouter related_name car sinon ça plante comme j'ai DEUX users en clé étrangère
    user_helper = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                    blank=True, related_name='helped_schedules')

    def __str__(self):
        date_locale = timezone.localtime(self.date_help)
        return self.name_activity + " - " + date_locale.strftime("%d/%m/%Y")

    @property
    def is_expired(self):
        """
        Méthode qui permet de savoir si la date prévue pour cette activité est expirée :
        méthode utilisée directement dans le template
        :return True ou False
        """
        now = timezone.now()
        return now > self.date_help
