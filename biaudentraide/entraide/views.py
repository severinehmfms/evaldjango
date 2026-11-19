from selectors import SelectSelector

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from django.views import generic

from entraide.forms import ScheduleForm, UserSkillForm
from entraide.models import Skill, UserSkill, Schedule


def index(request):
    """
    Vue qui permet d'afficher,
     - les schedules qu'il a créé, pour un utilisateur connecté
     - les prochains schedules validés, pour un visiteur
    """
    user_connecte = request.user

    # Si l'utilisateur est connecté on va récupérer la liste des créneaux qu'il a créé que ce soit passé ou futur
    if user_connecte.is_authenticated:
        schedules_list = Schedule.objects.filter(user_creator=user_connecte).order_by("-date_help")

    # Si c'est un visiteur, on va récupérer tous les prochains créneaux où un utilisateur a proposé ses services
    else:
        schedules_list = (Schedule.objects  .filter(user_helper__isnull=False)
                                            .filter(date_help__gte=timezone.now())
                                            .order_by("-date_help"))

    context = {"schedules_list": schedules_list}
    return render(request, "entraide/index.html", context)


# Vue générique pour la page d'affichage des compétences
class SkillsView(generic.ListView):
    template_name = "entraide/allskills.html"
    context_object_name = "skill_list"

    def get_queryset(self):
        return Skill.objects.order_by("name_skill")


@login_required
def helpschedules_view(request):
    """
    Vue qui permet d'afficher pour un utilisateur, la liste des schedules créés par les autres, dans le futur,
    pour lesquels l'utilisateur connecté possède la compétence requise, et auxquels personne n'a encore répondu
    """

    user_connecte = request.user

    # On récupère la liste des éléments UserSkill correspondant à l'utilisateur connecté
    skills_existing = UserSkill.objects.filter(user=user_connecte)

    # On récupère la liste des ids des compétences de cet utilisateur (pour checker les bonnes cases à cocher)
    skills_existing_ids = skills_existing.values_list("skill_id", flat=True)

    schedules_list = []

    if user_connecte.is_authenticated:
        schedules_list = (Schedule.objects.exclude(user_creator=user_connecte).filter(skill__in=skills_existing_ids)
                          .filter(user_helper=None)
                          .filter(date_help__gte=timezone.now())
                          .order_by("-date_help"))

    if len(skills_existing_ids) == 0:
        messages.error(request,
                       "Merci de renseigner vos compétences pour pouvoir afficher les créneaux correspondants.")

    context = {"schedules_list": schedules_list}
    return render(request, "entraide/helpschedules.html", context)


@login_required
def help_view(request, schedule_id):
    """ Vue qui permet de renseigner l'utilisateur qui accepte d'aider"""
    schedule = get_object_or_404(Schedule, pk=schedule_id)

    schedule.user_helper = request.user
    schedule.save()

    messages.success(request, "L'aidant a bien été mis à jour pour ce créneau.")

    return redirect("entraide:helpschedules")


@login_required
def majskills_view(request):
    """
    Vue pour afficher la page de mise à jour des compétences de l'utilisateur
    """

    user_connecte = request.user

    # On récupère la liste des éléments UserSkill correspondant à l'utilisateur connecté
    skills_existing = UserSkill.objects.filter(user=user_connecte)

    # On récupère la liste des ids des compétences de cet utilisateur (pour checker les bonnes cases à cocher)
    skills_existing_ids = skills_existing.values_list("skill_id", flat=True)

    # Si on est en POST, on récupère le formulaire renseigné
    if request.method == "POST":
        # On va récupérer les compétences cochées dans le formulaire
        skill_chk = request.POST.getlist("skill_chk")

        # On va effacer toutes les compétences liées à cet utilisateur
        UserSkill.objects.filter(user=user_connecte).delete()

        # On va enregistrer les nouvelles compétences cochées
        for skill_id in skill_chk:
            UserSkill.objects.create(user=user_connecte, skill=Skill.objects.get(id=int(skill_id)))

        # On retourne sur la page index.html,en rajoutant un message de confirmation
        messages.success(request, "Les compétences ont bien été mises à jour.")

        # Redirection sur la page d'index
        return redirect("entraide:index")

    # Si on arrive sur le formulaire, on va afficher le formulaire vide
    else:
        # On récupère la liste des compétences existantes pour les cases à cocher du formulaire
        skill_list = Skill.objects.order_by("name_skill")

        # if request.method == "POST":
        return render(request, 'entraide/majskills.html', {
            'skill_list': skill_list,
            'skills_existing': skills_existing,
            'skills_existing_ids': skills_existing_ids,
        })

@login_required
def majskillsbis_view(request):
    """
    Vue pour afficher la page de mise à jour des compétences de l'utilisateur
    """

    user_connecte = request.user

    if request.method == "POST":
        form = UserSkillForm(request.POST,user_connected=user_connecte)

        if form.is_valid():
            user_skill = form.save(commit=False)
            user_skill.user = user_connecte
            user_skill.save()

            messages.success(request, "La compétence a bien été ajoutée.")
            return redirect("entraide:majskillsbis")
    else:
        # On récupère la liste des compétences existantes
        skill_list = Skill.objects.exclude().order_by("name_skill")

        # On récupère la liste des objets Skill reliés à l'utilisateur
        skills_existing = Skill.get_user_skills(user_connecte)

        # On rajoute l'utilisateur connecté au formulaire pour pouvoir modifier la liste déroulante
        form = UserSkillForm(user_connected=user_connecte)

        return render(request, 'entraide/majskillsbis.html', {
            'form': form,
            'skill_list': skill_list,
            'skills_existing': skills_existing
        })



@login_required
def addschedule_view(request):
    """
    Vue pour permettre à l'utilisateur de créer un créneau pour une activité
    """

    if request.method == "POST":

        form = ScheduleForm(request.POST, user_connected=request.user)

        if form.is_valid():

            # Récupération de la compétence requise
            skill = form.cleaned_data["skill"]

            # Récupération de l'intitulé de l'activité
            name_activity = form.cleaned_data["name_activity"]

            # Récupération du créneau (date)
            date_help = form.cleaned_data["date_help"]

            # Création du schedule
            Schedule.objects.create(
                skill=skill,
                name_activity=name_activity,
                date_help=date_help,
                user_creator=request.user
            )

            messages.success(request, "Le créneau a bien été ajouté.")
            return redirect("entraide:index")
    else:
        form = ScheduleForm(user_connected=request.user)

    return render(
        request,
        "entraide/addschedule.html",
        {"form": form}
    )


def login_view(request):
    """ Vue pour la connexion """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # On récupère l'url demandée pour retourner dessus et non sur la page d'accueil
            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("entraide:index")

    else:
        form = AuthenticationForm()

    return render(request, "entraide/login.html", {
        "form": form
    })


def logout_view(request):
    """ Vue pour la déconnexion"""
    if request.method == "POST":
        logout(request)

    return redirect("entraide:index")
