# les urls de l'application reviews
from django.urls import path
from reviews import views

urlpatterns = [
    path('', views.home, name = "reviews-accueil"),
    # pour l'instant je laisse un nom différent mais il faudra traquer les reviews-accueil à changer enhom ou inversement
    path('ticket/', views.ticket, name = "reviews-ticket"),
    path('critique/', views.critique),
    path('répondre/', views.repondre),
    path('mes posts/', views.mesPosts, name= "reviews-mesPosts"),
    path('mon flux/', views.monFlux),
    path("inscription/", views.inscription),
    path("abonnements/", views.abonnements),
    path("home/", views.home, name = "reviews-home"),
]