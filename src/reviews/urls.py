# les urls de l'application reviews
from django.urls import path
from . import views
from .views import (
FollowCreateView,
FollowDeleteView,
AnswerView,
MyPostsListView,
# TicketListView,
TicketDetailView,
TicketCreateView,
TicketUpdateView,
TicketDeleteView,
ReviewCreateView,
# ReviewListView,
ReviewDetailView,
ReviewUpdateView,
ReviewDeleteView,
FeedListView,
MyPostsListView,
)


urlpatterns = [
    path("connect/", views.connect, name = "reviews-connect"),
    # path("feed/", views.feed, name = "reviews-feed"),
    path('', FeedListView.as_view(), name = "reviews-feed"),
    path('reviews/review/', FeedListView.as_view(), name = "reviews"),
    path('myPosts/', MyPostsListView.as_view(), name = "reviews-myPosts"),

    # path('ticket/list', TicketListView.as_view(), name = "reviews-ticket-list"),
    path("ticket/<pk>/", TicketDetailView.as_view(), name = "reviews-ticket-detail"),
    path("ticket/create", TicketCreateView.as_view(), name = "ticket-create"),
    path("ticket/<pk>/update/", TicketUpdateView.as_view(), name = "ticket-update"),
    path("ticket/<pk>/delete/", TicketDeleteView.as_view(), name = "ticket-delete"),

    # path("ticket/<pk>/answer/", AnswerView.as_view(), name = "answer"),
    # si j'ajoute une page spéciale pour répondre à un ticket particulier (créer la CreateView etc.)
    # https://stackoverflow.com/questions/14351048/django-optional-url-parameters
    path("ticket/<ticket_id>/answer/", AnswerView.as_view(), name = "answer"),

    path("follow/", FollowCreateView.as_view(), name = "abonnements"),
    path("unfollow/<pk>/delete/", FollowDeleteView.as_view(), name = "unfollow-delete"),

    # path('review/list', ReviewListView.as_view(), name = "reviews-review-list"),
    path("review/<pk>/", ReviewDetailView.as_view(), name = "reviews-review-detail"),
    path("review/create", ReviewCreateView.as_view(), name = "review-create"),
    path("review/<pk>/update/", ReviewUpdateView.as_view(), name = "review-update"),
    path("review/<pk>/delete/", ReviewDeleteView.as_view(), name = "review-delete"),
    path("review/review-plus-ticket", views.ReviewPlusTicket, name = "review-plus-ticket"),
]