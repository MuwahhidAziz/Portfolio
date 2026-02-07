from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:cat>/", views.category, name="category"),
    path("listing/bid/<str:user>/<str:title>/", views.bid, name="bid"),
    path("listing/comment/<str:user>/<str:title>/", views.comment, name="comment"),
    path("listing/<str:title>/", views.listing, name="listing"),
    path("listing/end/<str:user>/<str:title>", views.end, name="end"),
    path("create/<str:user>/", views.create, name="create"),
    path("watch/<str:user>/<str:title>/", views.add, name="addwatch"),
    path("watch/<str:user>/", views.watch, name='watch'),
    path("watch/remove/<str:user>/<str:title>/", views.remove, name="remove")
]
