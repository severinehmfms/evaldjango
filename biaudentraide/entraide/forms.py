from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db.models import Model
from django.http import request

from entraide.models import Skill, UserSkill


class ScheduleForm(forms.Form):

    name_activity = forms.CharField(
        label="Activité",
        max_length=200,
        validators=[
            MaxLengthValidator(200)
        ],
    )

    # TODO Rajouter un validator pour vérifier que la date est bien dans le futur !
    date_help = forms.DateTimeField(
        label="Choisir la date prévue pour l'activité",
        required=True,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"type": "datetime-local"}
        )
    )

    # On crée dans un premier temps une liste déroulante avec TOUTES les compétences
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), label="Choisir la compétence requise pour cette activité")

    # On rajoute cette fonction d'initialisation (pour notre formulaire) pour pouvoir envoyer des arguments au formulaire (dans mon cas : l'utilisateur connecté!)
    def __init__(self, *args, **kwargs):
        # On récupère l'utilisateur passé depuis la vue
        user_connected = kwargs.pop('user_connected', None)
        super().__init__(*args, **kwargs)

        if (user_connected):
            # print(f"User connected bien récupéré {user_connected.username}")

            # On récupère les compétences que possède l'utilisateur connecté
            skill_existing = UserSkill.objects.filter(user=user_connected).values_list('skill_id', flat=True)

            # On modifie le queryset du champ skill pour exclure les compétences de notre utilisateur !
            self.fields['skill'].queryset = Skill.objects.exclude(id__in=skill_existing)


