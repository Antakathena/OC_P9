from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
    )
from django.db.models import CharField, Value
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from datetime import datetime

from .forms import TicketForm, ReviewForm

from .models import Ticket, Review
from itertools import chain



def feed(request):
    date= datetime.today()
    username= request.user.username  #???
    reviews = Review.objects.all()
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.all()
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {
        'title':'home',
        'prenom': username,
        'date': date,
        'posts': posts,
    }
    return render(request, 'reviews/feed.html', context)

"""
class FeedView(ListView):
    model = Ticket
    template_name = 'feed.html'
    context_object_name = 'ticket_list'

    def get_context_data(self, **kwargs):
        context = super(FeedView, self).get_context_data(**kwargs)
        context.update({
            'reviews': Review.objects.order_by('-time_created'),
            'more_context': Review.objects.all(),
        })
        return context

    def get_queryset(self):
        return Ticket.objects.order_by('-time_created')
"""


def connect(request):
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
    return render(request,"reviews/connect.html", context )

class TicketListView(ListView):
    """
    Affiche les tickets créés.
    Remplace def ticket-list(request): return render(request,"reviews/home.html", context = {'tickets': Ticket.objects.all()})
    vue basée sur le tuto : https://www.youtube.com/watch?v=qDwdMDQ8oX4
    dans un dossier appName -> templates -> appName selon la convention Django
    """
    model = Ticket
    # template_name = 'reviews/monfichier.html' à indiquer si le template n'est pas nommé : <app>/<model>_<viewtype>.html
    context_object_name = 'tickets' # à indiquer si pas list.objects (vérif nom)
    ordering = ['-time_created'] # le "-" au début inverse l'ordre


class TicketDetailView(DetailView):
    """Affiche un ticket"""
    model = Ticket
    context_object_name = 'ticket'


class TicketCreateView(LoginRequiredMixin, CreateView):
    """Créer un ticket"""
    # ce ticket devra être affiché sur la page des utilisateurs abonnés
    model = Ticket
    form_class = TicketForm
    extra_context = {'action':"Créer votre ticket"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update un ticket"""
    # ce ticket devra être modifié sur la page des utilisateurs abonnés
    model = Ticket
    form_class = TicketForm
    extra_context = {'action':"Modifier votre ticket"}

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
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
        

class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    # template_name = reviews/review_list.html (superflux si son nom a la bonne syntaxe)
    ordering = ['-time_created'] # le "-" au début inverse l'ordre


class ReviewDetailView(LoginRequiredMixin, DetailView):
    """Affiche une review"""
    model = Review

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    créer un commentaire sur un ouvrage, en réponse à un ticket
    ou créer un ticket + commentaire associé dans le même geste
    NB : le ticket doit être rappelé en bas de la critique
    """
    model = Review
    form_class = ReviewForm
    # fields = ['ticket', 'rating', 'headline', 'body'] quand il n'y a rien à spécifier,
    # sinon, form dans form.py
    extra_context = {'action':"Ecrivez votre critique"}
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update une critique"""

    model = Review
    form_class = ReviewForm
    extra_context = {'action':"Modifier votre critique"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Supprimer une critique"""
    
    model = Review
    success_url = "/" 
    # ou "/feed/" ?

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
        

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