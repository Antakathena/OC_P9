from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def accueil(request):
    return HttpResponse("<h1>Connexion ou lien vers Inscription</h1>\
        <h2>Liste des pages disponibles :<br></h2>\
        <h3>Ecrire un post<br><br> Ecrire une critique<br><br> Repondre à une demande de critique<br><br>\
        Suivre mes Posts<br><br> Suivre mon Flux<br><br> Inscription<br><br> Suivre d'autres utilisateurs</h3>")

def post(request):
    return HttpResponse('<h1>lien inscription/connexion</h1> <p>Liste des pages disponibles</p>')

def critique(request):
    return HttpResponse('<h1>lien inscription/connexion</h1> <p>Liste des pages disponibles</p>')

def repondre(request):
    return HttpResponse('<h1>lien inscription/connexion</h1> <p>Liste des pages disponibles</p>')

def mesPosts(request):
    return HttpResponse('<h1>lien inscription/connexion</h1> <p>Liste des pages disponibles</p>')

def monFlux(request):
    return HttpResponse('<h1>lien inscription/connexion</h1> <p>Liste des pages disponibles</p>')

def inscription(request):
    return HttpResponse('<h1>lien inscription/connexion</h1> <p>Liste des pages disponibles</p>')
    
def suivre(request):
    return HttpResponse('<h1>lien inscription/connexion</h1> <p>Liste des pages disponibles</p>')