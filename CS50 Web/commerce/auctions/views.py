from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Auction, Bid, Comment, WatchList

import datetime
from decimal import Decimal

Choices = [
    ('None', 'None'),
    ('Home', 'Home'),
    ('Fashion', 'Fashion'),
    ('Toys', 'Toys'),
    ("Electronics", 'Electronics'),
    ('Stationary', 'Stationary'),
    ('Kitchen', 'Kitchen'),
    ('Food', 'Food'),
    ('Beverage', 'Beverage'),
    ('Agriculture', 'Agriculture'),
    ('Plant', 'Plant'),
    ('Pet', 'Pet'),
    ('Medical', 'Medical'),
    ('Detergents', 'Detergents'),
    ('Furniture', 'Furniture'),
    ('Automobile', 'Automobile'),
    ('Book', 'Book'),
    ('Misc', 'Misc')
]
class frm(forms.Form):
    title = forms.CharField(label="title", max_length=100)
    description = forms.CharField(label="description", widget=forms.Textarea)
    starting_bid = forms.DecimalField(label="starting bid", max_digits=10, decimal_places=2)
    image_url = forms.URLField(label="image url", required=False)
    category = forms.ChoiceField(label="category", required=False, choices=Choices)
        
class bfrm(forms.Form):
    amount = forms.DecimalField(label='Bid', max_digits=10, decimal_places=2)

    def __init__(self, *args, current=None, **kwargs):
        super().__init__(*args, **kwargs)
        if current is not None:
            self.fields['amount'].min_value = current

class cfrm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea)

def index(request):
    auctions = Auction.objects.all()
    if auctions:
        return render(request, "auctions/index.html", {"listings":auctions})
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, title):
    try:
        auction = Auction.objects.get(title=title)
        win = ''
        try:
            if not auction.active:
                win = auction.bids.get(amount=auction.current).bidder.username
        except Bid.DoesNotExist:
            pass
        return render(request, "auctions/listing.html", {"listing":auction, 'winner':win, 'comments':auction.comments.all(), "form":cfrm()})
    except Auction.DoesNotExist:
        return render(request, "auctions/404.html", {"message":f'Requested Listing "{title}" Not Found'})

@login_required
def end(request, user, title):
    act = Auction.objects.get(lister__username=user, title=title)
    act.active = False
    act.save()
    
    return HttpResponseRedirect(reverse("listing", kwargs={'title':title}))

@login_required
def bid(request, title, user):
    act = Auction.objects.get(title=title)
    if request.method == 'POST':
        usr = User.objects.get(username=user)
        amnt = Decimal(request.POST.get('amount'))
        print(type(act.current), type(amnt))
        if amnt <= act.current:
            return render(request, "auctions/bid.html", {'form':bfrm(current=act.current), 'title':title, 'Starting':act.starting_bid, 'Current':act.current, 'user':user, 'msg':f'Bid must be greater than ${act.current}'})
        if any(bds.auction.title == title for bds in usr.bids.all()):
            bd = usr.bids.get(auction__title=title)
            bd.amount = amnt

        else:
            bd = Bid(
                bidder=usr,
                auction=Auction.objects.get(title=title),
                amount=amnt
                )

        bd.save()

        return HttpResponseRedirect(reverse("listing", kwargs={'title':title}))

    if act.active and act.lister.username != user:
        bd = bfrm(current=act.current)
        return render(request, "auctions/bid.html", {'form':bd, 'title':title, 'Starting':act.starting_bid, 'Current':act.current, 'user':user})
    return HttpResponseRedirect(reverse("listing", kwargs={'title':title}))

@login_required
def create(request, user):
    if request.method == 'POST':
        listed = Auction(
            lister=User.objects.get(username=user),
            title=request.POST['title'],
            description=request.POST['description'],
            starting_bid=request.POST['starting_bid'],
            image_url=request.POST.get('image_url', ''),
            category=request.POST.get('category', None)
            )

        listed.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {'form':frm(), 'user':user})

@login_required
def watch(request, user):
    usr = User.objects.get(username=user)
    wls = usr.watchlist.all()
    return render(request, "auctions/watchlist.html", {'wls':wls})

def categories(request):
    cats = list(cat[0] for cat in Auction.choices)
    return render(request, "auctions/categories.html", {'categories':cats})

def category(request, cat):
    auctions = list(auct for auct in Auction.objects.all() if auct.category == cat)
    return render(request, "auctions/index.html", {'listings':auctions})

@login_required
def add(request, user, title):

    usr = User.objects.get(username=user)
    auct = Auction.objects.get(title=title)

    wl, created = WatchList.objects.get_or_create(
        user=usr,
        listing=auct
        )
    wl.save()

    return HttpResponseRedirect(reverse("watch", kwargs={'user':user}))

@login_required
def remove(request, user, title):
    usr = User.objects.get(username=user)
    usr.watchlist.get(listing__title=title).delete()
    return HttpResponseRedirect(reverse("watch", kwargs={'user':user}))

@login_required
def comment(request, user, title):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("listing", kwargs={'title':title}))

    act = Auction.objects.get(title=title)

    try:
        act.comments.commentor.username == user
        act.comments.comment = request.POST['comment']
        act.comments.save()
    except AttributeError:
        cm = Comment(
            commentor = User.objects.get(username=user),
            auction = act,
            comment = request.POST['comment']
            )
        cm.save()

    return HttpResponseRedirect(reverse("listing", kwargs={'title':title}))
