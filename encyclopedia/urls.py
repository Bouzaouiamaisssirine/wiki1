from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("crt", views.crt, name="crt"),
    path("wiki/<str:title>/change", views.editEntry, name="editEntry"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>/submit", views.submitEditEntry, name="submitEditEntry"),
    path("wiki/", views.randomEntry, name="randomEntry")
]
