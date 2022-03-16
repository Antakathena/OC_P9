# les urls de l'application reviews
from django.urls import path
from . import views
from .views import (
TicketListView,
TicketDetailView,
TicketCreateView,
TicketUpdateView,
TicketDeleteView,
ReviewCreateView,
ReviewListView,
ReviewDetailView,
ReviewUpdateView,
ReviewDeleteView
)


urlpatterns = [
    path("connect/", views.connect, name = "reviews-connect"),
    path("feed/", views.feed, name = "reviews-feed"),
    path('ticket/list', TicketListView.as_view(), name = "reviews-ticket-list"),
    path("ticket/<pk>/", TicketDetailView.as_view(), name = "reviews-ticket-detail"),
    path("ticket/create", TicketCreateView.as_view(), name = "ticket-create"),
    path("ticket/<pk>/update/", TicketUpdateView.as_view(), name = "ticket-update"),
    path("ticket/<pk>/delete/", TicketDeleteView.as_view(), name = "ticket-delete"),

    path('review/list', ReviewListView.as_view(), name = "reviews-review-list"),
    path("review/<pk>/", ReviewDetailView.as_view(), name = "reviews-review-detail"),
    path("review/create", ReviewCreateView.as_view(), name = "review-create"),
    path("review/<pk>/update/", ReviewUpdateView.as_view(), name = "review-update"),
    path("review/<pk>/delete/", ReviewDeleteView.as_view(), name = "review-delete"),
]