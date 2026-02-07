from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Auction, Bid, Comment, WatchList

#Customizations
class Listing(admin.ModelAdmin):
	list_display = ('title', 'category', 'active', 'starting_bid', 'description')
	search_fields = ('title', 'category', 'starting_bid', 'active', 'description')
	list_filter = ('category', 'active')
	ordering = ('starting_bid', 'active')

class Bidding(admin.ModelAdmin):
	list_display = ('auction', 'amount', 'timestamp')
	search_fields = ('amount', 'auction')
	list_filter = ('amount', 'auction')
	ordering = ('amount', 'timestamp')

class Remarks(admin.ModelAdmin):
	list_display = ('auction', 'comment')
	search_fields = ('auction',)

class Users(UserAdmin):
	list_display = ('username', 'email', 'is_staff', 'is_superuser', 'date_joined')
	search_fields = ('username', 'email')
	list_filter = ('username', 'email', 'date_joined', 'is_superuser', 'is_staff')
	ordering = ('date_joined',)

# Register your models here.
admin.site.register(User, Users)
admin.site.register(Auction, Listing)
admin.site.register(Bid, Bidding)
admin.site.register(Comment, Remarks)
admin.site.register(WatchList)