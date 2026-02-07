from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
class User(AbstractUser):
	points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	
	def __str__(self):
		return f"{self.username}"

class Product(models.Model):
	"""Model for Managing Products"""
	CHOICES = [
		('General', 'General'),
		('Dry Fruits', 'Dry Fruits'),
		('Home Made', 'Home Made'),
		('Fast Food', 'Fast Food'),
		('Fruits', 'Fruits'),
		('Vegetables', 'Vegetables')
	]

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	variants = models.JSONField(default=dict)
	category = models.CharField(max_length=50, choices=CHOICES, default='General')

	main_image = models.ImageField(upload_to='products/')
	image1 = models.ImageField(upload_to='products/', blank=True, null=True)
	image2 = models.ImageField(upload_to='products/', blank=True, null=True)
	image3 = models.ImageField(upload_to='products/', blank=True, null=True)
	image4 = models.ImageField(upload_to='products/', blank=True, null=True)
	image5 = models.ImageField(upload_to='products/', blank=True, null=True)
	
	def __str__(self):
		return f"{self.category.title()}:{self.title.title()}"

	@property
	def desc(self):
		return self.description[:20] + ('' if len(self.description) <= 20 else '...')

class Purchase(models.Model):
	"""Model for Blockchain Transaction Style Purchases"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
	quantity = models.IntegerField(validators=[MinValueValidator(1)])
	timestamp = models.DateTimeField(auto_now_add=True)
	size = models.CharField(max_length=10)
	bill = None

	def __str__(self):
		return f"{self.user.username} bought {self.product.title} x{self.quantity}"

class Cart(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user.username}'s Cart"

	@property
	def bill(self):
		return sum(item.bill for item in self.items.all())
	

class Item(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	size = models.CharField(max_length=10)
	quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

	def __str__(self):
		return f"{self.product.title.title()} x{self.quantity}"

	@property
	def bill(self):
		return self.product.variants[self.size] * self.quantity
	