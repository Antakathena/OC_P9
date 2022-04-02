from re import template
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from django.db.models import CharField, Value
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required

from itertools import chain
from datetime import datetime

from users.forms import *
from .forms import TicketForm, ReviewForm, ReviewAnswerForm, FollowForm
from .models import Ticket, Review, UserFollows

def connect(request): # ou View?
    """
    présentation du site et menu détaillé
    possibilité de se connecter
    renvoi vers s'inscrire
    """
    date = datetime.today()
    form = AuthenticationForm(request, data=request.POST)
    context = {
        'title':'connect',
        'prenom':'Sophie',
        'date': date,
        'tickets': Ticket.objects.all(),
        'form': form,
    }
    if request.method == "POST":

        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('/')
             
    return render(request,"reviews/connect.html", context )

class FeedListView(LoginRequiredMixin, ListView):
    """
    Récupère les Reviews et les Tickets et les range du plus récent au plus vieux
    En fait, j'ai fait comme si pas ListView et en commentaire,
    def feed(request): ...     return render(request, 'reviews/feed.html', context)
    comment il aurait vraiment fallu faire avec ListView
    """
    model = Ticket
    template_name = 'reviews/feed.html'
    # context_object_name = 'ticket_list'
    
    def get_context_data(self, **kwargs):
        """
        """
        date= datetime.today()
        username= self.request.user.username
        reviews = Review.objects.all()
        # returns queryset of reviews
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets = Ticket.objects.all()
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
        # returns queryset of tickets
        # ou plus adapté à POO ? : def get_queryset(self):
        # return Ticket.objects.order_by('-time_created')

        answered = []
        for review in reviews:
            answered.append(review.ticket)

        # combine and sort the two types of posts
        posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
        )

        context = super(FeedListView, self).get_context_data(**kwargs)
        context.update({
            # 'reviews': Review.objects.order_by('-time_created'),
            # 'more_context': Review.objects.all(),
            'title':'feed',
            'username': username,
            'date': date,
            'posts': posts,
            'answered': answered
        })
        return context


class MyPostsListView(LoginRequiredMixin,ListView):
    """
    tous mes tickets et critiques pour pouvoir :
    suivre les réponses (même de gens auxquels je ne suis pas abonné),
    les modifier et
    les supprimer
    """
    model = Ticket
    template_name = 'reviews/myPosts.html'
    context_object_name = 'ticket_list'
    
    
    def get_context_data(self, **kwargs):
        date= datetime.today()
        user= self.request.user
        username= self.request.user.username
        # get the :
        logged_in_user_reviews = Review.objects.filter(user=user)
        logged_in_user_reviews = logged_in_user_reviews.annotate(content_type=Value('REVIEW', CharField()))
        # and the :
        logged_in_user_tickets = Ticket.objects.filter(user=user)
        logged_in_user_tickets = logged_in_user_tickets.annotate(content_type=Value('TICKET', CharField()))
        answered = []
        for review in logged_in_user_reviews:
            answered.append(review.ticket)

        # combine and sort the two types of posts
        posts = sorted(
        chain(logged_in_user_reviews, logged_in_user_tickets),
        key=lambda post: post.time_created,
        reverse=True
        )

        context = super(MyPostsListView, self).get_context_data(**kwargs)
        context.update({
            # 'reviews': Review.objects.order_by('-time_created'),
            # 'more_context': Review.objects.all(),
            'title':'myPosts',
            'username': username,
            'date': date,
            'posts': posts,
            'answered': answered
        })
        return context

    def get_queryset(self):
        # return Ticket.objects.order_by('-time_created')
        pass


"""
class TicketListView(ListView):
    
    Affiche les tickets créés.
    Remplace def ticket-list(request): return render(request,"reviews/home.html", context = {'tickets': Ticket.objects.all()})
    vue basée sur le tuto : https://www.youtube.com/watch?v=qDwdMDQ8oX4
    dans un dossier appName -> templates -> appName selon la convention Django
    
    model = Ticket
    # template_name = 'reviews/monfichier.html' à indiquer si le template n'est pas nommé : <app>/<model>_<viewtype>.html
    context_object_name = 'tickets' # à indiquer si pas list.objects (vérif nom)
    ordering = ['-time_created'] # le "-" au début inverse l'ordre
"""


class TicketDetailView(LoginRequiredMixin,DetailView):
    """Affiche un ticket"""
    model = Ticket
    extra_context = {'reviews': Review.objects.all()}


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


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Supprimer un ticket"""
    model = Ticket
    success_url = "/"
    print(f'success_url: {success_url}')
    # pourquoi marchait précédemment avec ../.. ? (mais c'est mieux comme ça)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
        
"""
class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    # template_name = reviews/review_list.html (superflux si son nom a la bonne syntaxe)
    ordering = ['-time_created'] # le "-" au début inverse l'ordre
"""

class ReviewDetailView(LoginRequiredMixin, DetailView):
    """Affiche une review"""
    model = Review


class ReviewCreateView(LoginRequiredMixin, CreateView,):
    """
    créer un commentaire sur un ouvrage, en réponse à un ticket
    """
    model = Review
    form_class = ReviewForm
    # fields = ['ticket', 'rating', 'headline', 'body'] quand il n'y a rien à spécifier,
    # sinon, form dans form.py
    extra_context = {'action':"Répondre à un ticket"}
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def ReviewPlusTicket(request):  # class ReviewPlusTicketCreateView(LoginRequiredMixin, CreateView,)
    """
    créer un commentaire sur un ouvrage sans ticket, en créant le ticket
    """
    ticket_form = TicketForm()
    # sauf qu'il ne faut que le titre, la description doit être remplie automatiquement
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        review_form = ReviewForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            print(ticket.id)
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('/')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
}
    return render(request, 'reviews/review-plus-ticket-form.html', context=context)
    

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


class AnswerView(LoginRequiredMixin, CreateView):
    """
    écrire une critique en réponse à un ticket spécifique
    """

    model = Review
    template = "answer.html"
    form_class = ReviewAnswerForm
    
    # l'idée : si "répondre" a été cliqué au bas d'un ticket, on aura un ticket.id envoyé par le html via l'url
    extra_context = {'action':"Repondez à la demande", "ticket_id : "}

    def get_initial(self):
        """returns the initial data to use for forms on this view"""
        try:
            initial = super(AnswerView, self).get_initial()
            if ticket_id:
                initial['ticket'] = self.request.POST["ticket_id"] # à moins qu'il faille le mettre dans context
        except Exception as e: print(e)

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(AnswerView, self).get_form_kwargs()
    #     print(f"voilà les kwargs : {kwargs}")
    #     kwargs['ticket_id']=self.request.POST["ticket_id"] # POST est c un dico des données passées en POST

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(f"voilà les kwargs : {self.kwargs}")

        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Supprimer une critique"""
    
    model = Review
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class FollowCreateView(LoginRequiredMixin, CreateView):
    # manque id pour que ça enregistre bien - a corriger? 
    """
    page où je peux:
    retrouver la liste des utilisateurs auxquels je suis abonné,
    suivre un nouvel utisateur (à trouver par le nom dans une case, pas de registre demandé),
    me désabonner de quelqu'un
    """
    model = UserFollows
    template_name = 'reviews/follow.html'
    form_class = FollowForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        # comment exclure des choix les utilisateurs déjà suivis?
        kwargs = super(FollowCreateView, self).get_form_kwargs()
        kwargs['username']=self.request.user.username
        kwargs['following']=self.request.user.following.all()
        kwargs['followed_by']=self.request.user.followed_by.all()
        # bob = self.request.user.following.all()
        # for elt in bob:
        #     print(elt)
        # print(f"tu vas marcher...{bob}")
        return kwargs
    
    def get_context_data(self, **kwargs):
        following = self.request.user.following.all()
        # return queryset of follower
        followed_by = self.request.user.followed_by.all()
        context = super(FollowCreateView, self).get_context_data(**kwargs)
        context.update({
            'title':'abonnements',
            'following': following,
            'followed_by': followed_by,
        })
        return context

    # def get_queryset(self):
    #     return Profile.objects.all().exclude(user=self.request.user)

class FollowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Ne plus suivre un utilisateur
    """
    model = UserFollows
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
