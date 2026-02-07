from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path("", views.index, name='index'),
	path("register/", views.register, name="register"),
	path("login/", views.login_, name='login'),
	path("logout/", views.logout_, name='logout'),
	path("cart/", views.cart, name="cart"),
	path("order/", views.order, name="order"),
	path("store/", views.store, name="store"),
	path("<str:cat>/", views.category, name='category'),
	path("<str:cat>/<str:title>/", views.product, name='product'),
	path("<str:cat>/<str:title>/add", views.add_cart, name='add'),
	path("<str:cat>/<str:title>/<str:size>/remove", views.remove_cart, name='remove')
]