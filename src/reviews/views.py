from dataclasses import fields
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
from .forms import (
    TicketForm,
    ReviewForm,
    ReviewAnswerForm,
    FollowForm,
    TicketPlusReviewForm,
    ReviewPlusTicketForm
    )
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
    comment aurait-il vraiment fallu faire avec ListView ? pistes en commentaire
    """
    model = Ticket
    template_name = 'reviews/feed.html'
    # context_object_name = 'ticket_list'
    
    def get_context_data(self, **kwargs):
        """
        """
        date= datetime.today()
        username= self.request.user.username
        following = self.request.user.following.all().values_list()
        following_id =[]
        for elt in self.request.user.following.all().values_list() :
            # ceux que l'on suit
            following_id.append(elt[-1])

        reviews = Review.objects.filter(user_id__in=following_id) # .filter()
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets = Ticket.objects.filter(user_id__in=following_id) # .filter(user=following ?)
        print(f'voici les tickets au complet : {Ticket.objects.all().values()}')
        print(f'voici following.all() : {following_id}')
        print(f'voici un essai pour récupérer les tickets des suivis : {Ticket.objects.filter(user_id__in=following_id)}')

        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
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
            'answered': answered,
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
        # and get the answer to our tickets :
        review_to_our_tickets = Review.objects.filter(ticket__in=logged_in_user_tickets)
        review_to_our_tickets = review_to_our_tickets.annotate(content_type=Value('REVIEW', CharField()))

        
        # check if a ticket already has an answer
        reviews = Review.objects.all()
        answered = []
        for review in reviews:
            answered.append(review.ticket)

        # combine and sort the two types of posts
        posts = sorted(
        chain(logged_in_user_reviews, logged_in_user_tickets, review_to_our_tickets),
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
            'answered': answered,
            'review_to_our_tickets': review_to_our_tickets,
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


def get_reviews_ticket(self):
        """
        (sert à récupérer review.ticket_id quand on a le pk d'une review)
        Pour review_update et delete : donne l'id du ticket de la critique
        """
        pk = self.kwargs.get("pk") # récupère l'id de la review
        review = Review.objects.filter(id=pk) # récupère la review, queryset (itérable)
        qs_ticket_id = review.values_list('ticket_id', flat=True) # ticket_id = <QuerySet [31]>
        ticket_id = qs_ticket_id.first() # = la valeur et non un queryset
        return ticket_id

@login_required
def ReviewPlusTicket(request):  # class ReviewPlusTicketCreateView(LoginRequiredMixin, CreateView,)
    """
    créer un commentaire sur un ouvrage sans ticket, en créant le ticket
    """
    ticket_form = TicketPlusReviewForm()
    review_form = ReviewPlusTicketForm()

    if request.method == 'POST':
        ticket_form = TicketPlusReviewForm(request.POST)
        review_form = ReviewPlusTicketForm(request.POST, request.FILES)
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
    form_class = ReviewAnswerForm
    extra_context = {'action':"Modifier votre critique", "ticket" : "déterminé"}
    # "ticket" : "déterminé" sert à dire au template s'il doit afficher ou non un bouton.
    
    def get_initial(self):
        """returns the initial data to use for forms on this view"""
        ticket_id= get_reviews_ticket(self)

        try:
            initial = super().get_initial()
            initial['ticket'] = ticket_id
        except Exception as e:
            print(e)
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        """
        Détermine les arguments nommés qui seront envoyés au __init__ de form_class
        via form_class(**self.get_form_kwargs())
        """
        ticket_id= get_reviews_ticket(self)

        kwargs = super().get_form_kwargs()
        kwargs["ticket_id"] = ticket_id
        return kwargs 

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
    form_class = ReviewAnswerForm
    
    # l'idée : si "répondre" a été cliqué au bas d'un ticket, on aura un ticket.id envoyé par le html via l'url
    extra_context = {'action':"Vous pouvez répondre à la demande", "ticket" : "déterminé"}

    def get_initial(self):
        """returns the initial data to use for forms on this view"""
        try:
            initial = super().get_initial() # la forme explicite de super() avec super(ReviewAnswerForm, self) est datée
            initial['ticket'] = self.kwargs.get("ticket_id")
        except Exception as e:
            print(e)
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        """
        Détermine les arguments nommés qui seront envoyés au __init__ de form_class
        via form_class(**self.get_form_kwargs())
        """
        kwargs = super().get_form_kwargs()
        # les kwargs passés à la vue sont bien dans self.kwargs
        # get_form_kwargs sert à les transmettre au constructeur du formulaire
        # cf https://github.com/django/django/blob/main/django/views/generic/edit.py#L39
        kwargs["ticket_id"] = self.kwargs.get("ticket_id")
        # étudier .get() et .POST[]
        # POST est c un dico des données passées en POST
        return kwargs 

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
