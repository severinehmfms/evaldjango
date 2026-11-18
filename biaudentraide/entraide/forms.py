from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from entraide.models import Skill


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

    # TODO Il faut pouvoir choisir ici UNIQUEMENT les compétences que l'utilisateur n'a pas !
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), label="Choisir la compétence requise pour cette activité")

