from django.shortcuts import render
from .models import Product, Category
# pagination
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'shop/listing.html')

def all_products(request):
    products_all = Product.objects.all().filter(available=True)
    paginator = Paginator(products_all, 8)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except(EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    ctx = {'products': products}
    return render(request, 'shop/listing.html', ctx)

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    ctx = {'product': product}
    return render(request, 'shop/detail.html', ctx)
