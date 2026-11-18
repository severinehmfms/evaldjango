from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views import generic

from entraide.models import Skill, UserSkill


# Vue générique pour la page index (qui affiche la liste des compétences)
class IndexView(generic.ListView):
    template_name = "entraide/index.html"
    context_object_name = "skill_list"

    def get_queryset(self):
        return Skill.objects.order_by("name_skill")


@login_required
def majskills_view(request):
    # On récupère l'utilisateur connecté
    user_connecte = request.user

    # On récupère la liste des éléments UserSkill correspondant à l'utilisateur connecté
    skills_existing = UserSkill.objects.filter(user=user_connecte)
    skills_existing_ids = skills_existing.values_list("skill_id", flat=True)

    if request.method == "POST":
        # On va récupérer les compétences cochées dans le formulaire
        skill_chk = request.POST.getlist("skill_chk")

        # On va effacer toutes les compétences liées à cet utilisateur
        UserSkill.objects.filter(user=user_connecte).delete()

        # On va enregistrer les nouvelles compétences cochées
        for skill_id in request.POST.getlist("skill_chk"):
            UserSkill.objects.create(user=user_connecte, skill=Skill.objects.get(id=int(skill_id)))

        # On retourne sur la page index.html,en rajoutant un message de confirmation
        messages.success(request, "Les compétences ont bien été mises à jour.")

        # Redirection sur la page d'index
        return redirect("entraide:index")

    else:
        # On récupère la liste des compétences existantes pour les cases à cocher du formulaire
        skill_list = Skill.objects.order_by("name_skill")

        # if request.method == "POST":
        return render(request, 'entraide/majskills.html', {
            'skill_list': skill_list,
            'skills_existing': skills_existing,
            'skills_existing_ids': skills_existing_ids,
        })



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