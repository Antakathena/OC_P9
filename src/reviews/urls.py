# les urls de l'application reviews
from django.urls import path
from . import views
from .views import (TicketListView,
TicketDetailView,
TicketCreateView,
TicketUpdateView,
TicketDeleteView
)


urlpatterns = [
    path("home/", views.home, name = "reviews-home"),
    path('', TicketListView.as_view(), name = "reviews-ticketList"),
    # pour l'instant je laisse un nom différent mais il faudra traquer les reviews-accueil à changer enhom ou inversement
    path("ticket/<pk>/", TicketDetailView.as_view(), name = "reviews-ticket-detail"),
    path("demande", TicketCreateView.as_view(), name = "ticket-create"),
    path("ticket/<pk>/update/", TicketUpdateView.as_view(), name = "ticket-update"),
    path("ticket/<pk>/delete/", TicketDeleteView.as_view(), name = "ticket-delete"),
]