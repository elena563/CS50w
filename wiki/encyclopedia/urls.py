from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("random/", views.random, name="random"),
    path("edit/<str:title>/", views.edit, name="edit")
]
