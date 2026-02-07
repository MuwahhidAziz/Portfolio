from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Purchase, Cart, Item
# Register your models here.

class Users(UserAdmin):
	list_display = ('username', 'email', 'points', 'is_staff', 'is_superuser', 'date_joined')
	search_fields = ('username', 'email', 'points')
	list_filter = ('username', 'points', 'date_joined', 'is_superuser', 'is_staff')
	ordering = ('date_joined',)

class Products(admin.ModelAdmin):
	list_display = ('title', 'variants', 'category')
	search_fields = ('title', 'category')
	list_filter = ('title', 'variants', 'category')
	ordering = ('variants',)

class Transaction(admin.ModelAdmin):
	list_display = ('user', 'product', 'quantity', 'size', 'bill')
	search_fields = ('user', 'product', 'quantity', 'size', 'bill', 'timestamp')
	list_filter = ('user', 'product', 'quantity', 'size', 'timestamp')

admin.site.register(User, Users)
admin.site.register(Product, Products)
admin.site.register(Purchase, Transaction)
admin.site.register(Cart)
admin.site.register(Item)