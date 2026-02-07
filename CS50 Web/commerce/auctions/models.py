from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    choices = [
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
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True, choices=choices)
    active = models.BooleanField(default=True)

    @property
    def current(self):
        bids = self.bids.all()
        if bids.exists():
            return max([bid.amount for bid in bids])
        return self.starting_bid

    def __str__(self):
        return f'{self.title}: Starting at ${self.starting_bid}, Currently ${self.current}'

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bidder.username} bid ${self.amount} on {self.auction.title} at {self.timestamp}'

class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()

    def __str__(self):
        cmnt = self.comment[:30] + ('' if len(self.comment) <= 30 else '...')
        return f'{self.commentor.username} commented on {self.auction.title}: {cmnt}'

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='watchlist')
    
    def __str__(self):
        return f'{self.listing.title} is in watchlist of {self.user.username}'