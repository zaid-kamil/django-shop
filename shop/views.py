from django.shortcuts import render
from .models import Product, Category
# Create your views here.
def index(request):
    return render(request, 'shop/listing.html')

def all_products(request):
    products = Product.objects.all().filter(available=True)
    ctx  = {'products': products}
    return render(request, 'shop/listing.html', ctx)
