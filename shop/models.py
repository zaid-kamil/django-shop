from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    token = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='USD Order Total')
    emailAddress = models.EmailField(max_length=255, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='USD Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def sub_total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return self.product
    
class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

class Payment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    

