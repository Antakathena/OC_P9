# les urls de l'application reviews
from django.urls import path
from . import views
# les vues Connect et ReviewPlusTicket sont des function based views
# les autres des Class Based Views
from .views import (
    FollowCreateView,
    FollowDeleteView,
    FeedListView,
    MyPostsListView,
    TicketDetailView,
    TicketCreateView,
    TicketUpdateView,
    TicketDeleteView,
    ReviewCreateView,
    ReviewDetailView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewToSpecificTicketView,
    )


urlpatterns = [
    path("connect/", views.connect, name="reviews-connect"),

    path("follow/", FollowCreateView.as_view(), name="abonnements"),
    path("unfollow/<pk>/delete/", FollowDeleteView.as_view(), name="unfollow-delete"),

    path('', FeedListView.as_view(), name="reviews-feed"),
    path('reviews/review/', FeedListView.as_view(), name="reviews"),
    path('myPosts/', MyPostsListView.as_view(), name="reviews-myPosts"),

    path("ticket/<pk>/", TicketDetailView.as_view(), name="reviews-ticket-detail"),
    path("ticket/create/", TicketCreateView.as_view(), name="ticket-create"),
    path("ticket/<pk>/update/", TicketUpdateView.as_view(), name="ticket-update"),
    path("ticket/<pk>/delete/", TicketDeleteView.as_view(), name="ticket-delete"),

    path("review/<pk>/", ReviewDetailView.as_view(), name="reviews-review-detail"),
    path("review/create/", ReviewCreateView.as_view(), name="review-create"),
    path("review/<pk>/update/", ReviewUpdateView.as_view(), name="review-update"),
    path("review/<pk>/delete/", ReviewDeleteView.as_view(), name="review-delete"),
    path("review/review-plus-ticket/", views.review_plus_ticket, name="review-plus-ticket"),
    path("ticket/<ticket_id>/answer/", ReviewToSpecificTicketView.as_view(), name="answer"),
]

