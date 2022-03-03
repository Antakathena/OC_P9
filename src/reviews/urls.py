# les urls de l'application reviews
from django.urls import path
from reviews import views

urlpatterns = [
    path('', views.accueil, name = "reviews-accueil"),
    path('ticket/', views.ticket, name = "reviews-ticket"),
    path('critique/', views.critique),
    path('répondre/', views.repondre),
    path('mes posts/', views.mesPosts, name= "reviews-mesPosts"),
    path('mon flux/', views.monFlux),
    path("inscription/", views.inscription),
    path("abonnements/", views.abonnements),
    path("home/", views.home, name = "reviews-home"),
]