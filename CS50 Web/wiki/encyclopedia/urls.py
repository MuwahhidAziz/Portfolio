from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("random/", views.rndm, name="random"),
    path("wiki/<str:TITLE>/", views.display, name="display"),
    path("edit/<str:TITLE>/", views.edit, name='edit'),
    path("results/", views.result, name="results")
]
