from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from django.views import generic

from entraide.forms import ScheduleForm
from entraide.models import Skill, UserSkill, Schedule


def index(request):
    """
        user_connecte = request.user
        if (user_connecte.is_authenticated):
    """
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # context = {"latest_question_list": latest_question_list}
    context = {"test": "test"}
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))
    # Raccourci pour les deux dernières lignes commentées :
    return render(request, "entraide/index.html", context)


# Vue générique pour la page d'affichage des compétences
class SkillsView(generic.ListView):
    template_name = "entraide/allskills.html"
    context_object_name = "skill_list"

    def get_queryset(self):
        return Skill.objects.order_by("name_skill")


def showschedules_view(request):

    # schedules_list = Schedule.objects.all().order_by("-date_help")

    # On récupère la liste des schédules dont la date_help est après la date du jour.
    schedules_list = Schedule.objects.filter(date_help__gte=timezone.now()).order_by("-date_help")


    # on verra plus tard... Si l'utilisateur est connecté on va récupérer la liste de ses créneaux

    # Si c'est un visiteur, on va récupérer tous les prochains créneaux (en anomysant les personnes)



    context = {"schedules_list": schedules_list}
    return render(request, "entraide/showschedules.html", context)


"""
Vue pour afficher la page de mise à jour des compétences de l'utilisateur
"""
@login_required
def majskills_view(request):
    # On récupère l'utilisateur connecté
    user_connecte = request.user

    # On récupère la liste des éléments UserSkill correspondant à l'utilisateur connecté
    skills_existing = UserSkill.objects.filter(user=user_connecte)

    # On récupère la liste des ids des compétences de cet utilisateur (plus simple pour checker les bonnes cases à cocher)
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


"""
Vue pour permettre à l'utilisateur de créer un créneau pour une activité 
"""
@login_required
def addschedule_view(request):

    if request.method == "POST":

        form = ScheduleForm(request.POST,user_connected=request.user)

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
                date_help=date_help
            )

            messages.success(request, "Le créneau a bien été ajouté.")
            # Sans le raccourci
            # return HttpResponseRedirect(reverse("polls:index"))
            # En utilisant le raccourci de from django.shortcuts import redirect
            return redirect("entraide:index")
    else:
        form = ScheduleForm(user_connected=request.user)

    return render(
        request,
        "entraide/addschedule.html",
        {"form": form}
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # On récupère l'url demandée pour retourner dessus et non sur la page d'accueil
            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("entraide:majskills")

    else:
        form = AuthenticationForm()

    return render(request, "entraide/login.html", {
        "form": form
    })


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("entraide:index")