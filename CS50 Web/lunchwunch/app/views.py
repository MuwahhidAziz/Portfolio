from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve, Resolver404
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Product, Purchase, Cart, Item

cats = tuple(cat[0] for cat in Product.CHOICES)

# utility
def redirector(request):
	try:
		match = resolve(request.session.get('last_visited', '/'))
		resolved = reverse(match.view_name, args=match.args, kwargs=match.kwargs)
		print(match.view_name, '...redirecting to last visited')
	except Resolver404 as e:
		resolved = reverse('index')
	return HttpResponseRedirect(resolved)

def cart_check(request, product):
	try:
		if cart := request.user.cart:
			if item := cart.items.get(product__title=product.title, product__category=product.category):
				return item.quantity, 'Update Cart!'
	except Exception:
		pass
	return 1, 'Add to Cart!'

# Create your views here.
def register(request):
	if request.method == 'POST':
		name, email, pas, cnfrm = request.POST['username'], request.POST['email'], request.POST['password'], request.POST['confirmation']
		if pas != cnfrm:
			return render(request, 'app/register.html', {'message':'Confirmed password doesnot match.'})

		try:
			user = User.objects.create_user(name, email, pas)
			user.save()
		except IntegrityError:
			return render(request, 'app/register.html', {'message':'Username already exists, try logging in or different username.'})

		login(request, user)
		return redirector(request)

	return render(request, 'app/register.html')
def login_(request):
	if request.method == 'POST':
		name, pas = request.POST['username'], request.POST['password']
		user = authenticate(request, username=name, password=pas)

		message = ''

		if not (name or pas):
			if name:
				message = 'Please Provide the Password as well.'
			elif pas:
				message = 'Please Provide the Username.'
			else:
				message = 'Please Provide Username and Password.'

		elif user is None:
			message = 'Invalid Username and/or Password.'

		if message:
			return render(request, 'app/login.html', {'message':message})
		
		login(request, user)
		return redirector(request)

	return render(request, 'app/login.html')

def logout_(request):
	logout(request)
	return redirector(request)

def index(request):
	request.session['last_visited'] = '/'
	return render(request, 'app/index.html')

def store(request):
	global cats
	request.session['last_visited'] = '/store/'
	return render(request, 'app/store.html', {'categories':cats})

def category(request, cat):
	global cats
	if cat in cats:
		prods = Product.objects.filter(category=cat)
		request.session['last_visited'] = f'/{cat}'
		return render(request, 'app/category.html', {'category':cat, 'products':prods})
	return render(request, 'app/404.html', {'target':f'category "{cat}"'})

def product(request, cat, title):
	try:
		p = Product.objects.get(category=cat, title=title)
		v, t = cart_check(request, p)
		request.session['last_visited'] = f'/{cat}/{title}'
		return render(request, 'app/product.html', {'product':p, 'value':v, 'text':t})
	except Product.DoesNotExist:
		return render(request, 'app/404.html', {'target':f'"{cat}" category, "{title}" product'})

@login_required
def add_cart(request, cat, title):
	if request.method == 'POST':
		size = request.POST.get('size')

		try:
			p = Product.objects.get(title=title, category=cat)
		except (Product.DoesNotExist, ObjectDoesNotExist):
			return render(request, 'app/404.html', {'target':f'"{cat}" category, "{title}" product'})
		
		cart, c = Cart.objects.get_or_create(user=request.user)
		item, i = cart.items.get_or_create(product=p, cart=cart, size=size)

		item.quantity = int(request.POST.get('quantity', 1))

		cart.save()
		item.save()

	return redirector(request)

@login_required
def remove_cart(request, cat, title, size):
	if request.method == "POST":
		try:
			request.user.cart.items.get(product__title=title, product__category=cat, size=size).delete()
		except ObjectDoesNotExist:
			pass
	return redirector(request)

@login_required
def cart(request):
	try:
		items = request.user.cart.items.all()
		bill = request.user.cart.bill
	except ObjectDoesNotExist:
		items = []
		bill = 0
	request.session['last_visited'] = f'/cart/'
	return render(request, 'app/cart.html', {'cart':items, 'bill':f'{bill:,}'})

@login_required
def order(request):
	if request.method == "POST":
		try:
			cart = request.user.cart
			request.user.points += (cart.bill // 100)
			for item in cart.items.all():
				Purchase(
					user=request.user,
					product=item.product,
					size=item.size,
					quantity=item.quantity,
					bill=item.bill
				).save()

		except Cart.DoesNotExist:
			pass
	return redirector(request)