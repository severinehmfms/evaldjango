from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.views import generic

from entraide.models import Skill

# Vue générique pour la page index (qui affiche la liste des compétences)
class IndexView(generic.ListView):
    template_name = "entraide/index.html"
    context_object_name = "skill_list"

    def get_queryset(self):
        return Skill.objects.order_by("name_skill")

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

            return redirect("entraide:index")

    else:
        form = AuthenticationForm()

    return render(request, "entraide/login.html", {
        "form": form
    })

def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("entraide:index")