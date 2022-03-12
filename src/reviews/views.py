from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.db.models import CharField, Value
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from datetime import datetime

from .models import Ticket, Review
from itertools import chain



"""
def feed(request):
    reviews = get_users_viewable_reviews(request.user)  
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'feed.html', context={'posts': posts})
"""

# nb : ce serait bien de pouvoir afficher les tickets et critiques en faisant une
# recherche par auteur, titre, etc. c'est quoi les champs déjà?

def home(request):
    """
    A terme :
    présentation du site et menu détaillé
    possibilité de se connecter
    renvoi vers ou possibilité de s'inscrire
    """
    date = datetime.today()
    # template = 'login'
    # trouver comment gérer sub-template inheritance pour importer login
    context = {
        'title':'home',
        'prenom':'Sophie',
        'date': date,
        'tickets': Ticket.objects.all(),
    }
    return render(request,"reviews/home.html", context )


class TicketListView(ListView):
    """
    Affiche les tickets créés.
    Remplace def ticket-list(request): return render(request,"reviews/home.html", context = {'tickets': Ticket.objects.all()})
    vue basée sur le tuto : https://www.youtube.com/watch?v=qDwdMDQ8oX4
    dans un dossier appName -> templates -> appName selon la convention Django
    """
    model = Ticket
    template_name = 'reviews/tickets.html' # à indiquer si le template n'est pas nommé : <app>/<model>_<viewtype>.html
    context_object_name = 'tickets' # à indiquer si pas list.objects (vérif nom)
    ordering = ['-time_created'] # le "-" au début inverse l'ordre


class TicketDetailView(DetailView):
    """Affiche un ticket"""
    model = Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    """Créer un ticket"""
    # ce ticket devra être affiché sur la page des utilisateurs abonnés
    model = Ticket
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update un ticket"""
    # ce ticket devra être modifié sur la page des utilisateurs abonnés
    model = Ticket
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
        # à écrire en 1 ligne ou laisser pour plus de lisibilité?

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Supprimer un ticket"""
    # ce ticket devra être supprimé de la page des utilisateurs abonnés
    model = Ticket
    success_url = "/home/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
        # à écrire en 1 ligne ou laisser pour plus de lisibilité?
        

def review(request):
    '''
    créer un commentaire sur un ouvrage, en réponse à un ticket
    ou créer un ticket + commentaire associé dans le même geste
    NB : le ticket doit être rapelé en bas de la critique
    '''
    # donc pour ça il faut pouvoir cliquer sur un bouton répondre
    # en bas de chaque ticket qu'on lit

    return render(request,"reviews/review.html", context = {'title':'review','ouvrage':'Madame Bovary'})

def mesPosts(request):
    """
    tous mes tickets et critiques pour pouvoir :
    suivre les réponses (même de gens auxquels je ne suis pas abonné),
    les modifier et
    les supprimer
    """
    #quelque chose comme for ticket in ticket + for critique in critique
    # (ajouter au context?) l'afficher dans la page
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    # return render(request,"mesPosts.html", context = {'tickets':tickets, 'critiques':critiques})
    return render(request,"reviews/mesPosts.html", context = {'tickets':tickets, 'critiques':reviews})

def feed(request):
    """
    les tickets et critiques des utilisateurs auxquels je suis abonné
    attention : exclure les posts de l'utilisateur connecté
    """
    # for utilisateur auquel je suis abonné, va chercher dans la base de donnée
    # ce qu'il a fait paraitre (donc il faut un tag "auteur"? comment c'est rangé dans la bd?)
    return HttpResponse('<h1>Mon Flux / Feed</h1>')


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