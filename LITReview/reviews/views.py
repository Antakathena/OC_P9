from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

# Create your views here.

def accueil(request):
    return HttpResponse("<h1>Connexion ou lien vers Inscription</h1>\
        <h2>Liste des pages disponibles :<br></h2>\
        <h3>Ecrire un post<br><br> Ecrire une critique<br><br> Repondre à une demande de critique<br><br>\
        Suivre mes Posts<br><br> Suivre mon Flux<br><br> Inscription<br><br> Suivre d'autres utilisateurs</h3>")

def post(request):
    template = get_template("ticket.html")
    page = template.render({"exemple": "coucou ! depuis views.py"})
    return HttpResponse(page)

def critique(request):
    return HttpResponse('<h1>Créer une critique</h1>')

def repondre(request):
    return HttpResponse('<h1>Répondre à une demande de critique</h1>')

def mesPosts(request):
    return HttpResponse('<h1>Suivre mes posts</h1>')

def monFlux(request):
    return HttpResponse('<h1>Mon Flux / Feed</h1>')

def inscription(request):
    return HttpResponse('<h1>Inscription</h1>')
    
def suivre(request):
    return HttpResponse('<h1>Suivre un utilisateur / Abonnements</h1>')