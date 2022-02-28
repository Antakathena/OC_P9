from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from datetime import datetime

# nb : ce serait bien de pouvoir afficher les tickets et critiques en faisant une
# recherche par auteur, titre, etc. c'est quoi les champs déjà?

def accueil(request):
    """
    présentation du site et menu détaillé
    possibilité de se connecter
    renvoi vers ou possibilité de s'inscrire
    """
    return render(request,"accueil.html")


def ticket(request):
    """
    poster un ticket pour demander une critique
    """
    # donc un input/formulaire qui permet de saisir une demande qui sera ajoutée
    # à la db avec l'information de la date, l'auteur, etc. pour pouvoir la retrouver
    # ce ticket sera affiché sur la page des utilisateurs abonnés
    date = datetime.today()
    return render(request,"ticket.html", context = {'prenom':'Sophie','date':date})
    template = get_template("ticket.html")
    page = template.render({"exemple": "coucou ! depuis views.py"})
    return HttpResponse(page)

def critique(request):
    """
    poster une critique a propos d'un livre
    """
    return render(request,"critique.html", context = {'titre':'Madame Bovary'})

def repondre(request):
    """
    poster une critique a propos d'un livre
    en réponse à un ticket
    """
    # donc pour ça il faut pouvoir cliquer sur un bouton répondre
    # en bas de chaque ticket qu'on lit
    return HttpResponse('<h1>Répondre à une demande de critique</h1>')

def mesPosts(request):
    """
    tous mes tickets et critiques pour pouvoir :
    suivre les réponses (même de gens auxquels je ne suis pas abonné),
    les modifier et
    les supprimer
    """
    #quelque chose comme for ticket in ticket + for critique in critique
    # (ajouter au context?) l'afficher dans la page
    return HttpResponse('<h1>Suivre mes posts</h1>')

def monFlux(request):
    """
    les tickets et critiques des utilisateurs auxquels je suis abonné
    """
    # for utilisateur auquel je suis abonné, va chercher dans la base de donnée
    # ce qu'il a fait paraitre (donc il faut un tag "auteur"? comment c'est rangé dans la bd?)
    return HttpResponse('<h1>Mon Flux / Feed</h1>')

def inscription(request):
    """
    formulaire d'inscription
    """
    # ça ça doit être du tout cuit dans Django, chercher
    return HttpResponse('<h1>Inscription</h1>')
    
def abonnements(request):
    """
    page où je peux:
    retrouver la liste des utilisateurs auxquels je suis abonné,
    suivre un nouvel utisateur (à trouver par le nom dans une case, pas de registre demandé),
    me désabonner de quelqu'un
    """
    # for utilisateur suivi dans abonnements, afficher utilisateur
    # ajouter à côté de chaque un bouton se désabonner
    # un input pour rentrer le nom d'un utilisateur pour s'y abonner (après verif qu'il est bien dans la db et récupération)
    return HttpResponse('<h1>Suivre un utilisateur / Abonnements</h1>')