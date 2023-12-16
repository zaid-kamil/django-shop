from django.shortcuts import render, redirect
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Payment, ShippingAddress, ProductImage
# pagination
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib import messages
# decorators
from django.contrib.auth.decorators import login_required



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

# cart views
def view_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        ctx = {'cart': cart}
    else:
        empty_message = 'Your cart is empty, please keep shopping.'
        ctx = {'empty': True, 'empty_message': empty_message}
    return render(request, 'shop/cart.html', ctx)

@login_required
def add_to_cart(request, pid):
    product = Product.objects.get(id=pid)
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        product_already_in_cart = cart.items.filter(product=product)
        # item already in cart
        if product_already_in_cart:
            cart_item = product_already_in_cart[0] # get the first item
            cart_item.quantity += 1
            cart_item.save()
        # new item in cart
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1, price=product.price)
            cart.items.add(cart_item)
        cart.save()
    # no cart yet
    else:
        cart = Cart.objects.create()
        print(product.price)
        cart_item = CartItem.objects.create(cart=cart, product=product,quantity=1, price=product.price)
        cart.items.add(cart_item)
        cart.save()
        request.session['cart_id'] = cart.id
    update_cart_counter(request)
    messages.success(request, 'The product was added to your cart.')
    # return to referring page
    return redirect(request.META['HTTP_REFERER'])

@login_required
def remove_from_cart(request, pid):
    product = Product.objects.get(id=pid)
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        product_already_in_cart = cart.items.filter(product=product)
        # item already in cart
        if product_already_in_cart:
            cart_item = product_already_in_cart[0]
            cart_item.quantity -= 1
            cart_item.save()
            # remove item from cart if quantity is 0
            if cart_item.quantity < 1:
                cart_item.delete()
        cart.save()
    messages.success(request, 'The product was removed from your cart.')
    # return to referring page
    return redirect(request.META['HTTP_REFERER'])

# order views
@login_required
def all_orders(request):
    orders = Order.objects.filter(user=request.user)
    ctx = {'orders': orders}
    return render(request, 'shop/orders.html', ctx)

@login_required
def create_order(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        order = Order.objects.create(user=request.user, cart=cart, total=cart.total)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, price=item.price, quantity=item.quantity)
        cart.delete()
        request.session['cart_id'] = None
        messages.success(request, 'Your order was created.')
    else:
        messages.info(request, 'You have no active cart.')
    return redirect('all_orders')

@login_required
def order_detail(request, oid):
    order = Order.objects.get(id=oid)
    ctx = {'order': order}
    return render(request, 'shop/order_detail.html', ctx)

# checkout views
@login_required
def checkout(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        ctx = {'cart': cart}
    else:
        empty_message = 'Your cart is empty, please keep shopping.'
        ctx = {'empty': True, 'empty_message': empty_message}
    return render(request, 'shop/checkout.html', ctx)

@login_required
def checkout_success(request):
    return render(request, 'shop/checkout_success.html')

@login_required
def checkout_cancelled(request):
    return render(request, 'shop/checkout_cancelled.html')

# payment views
@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    try:
        token = request.POST.get('stripeToken')
        payment = Payment.objects.create(user=request.user, token=token, order=order, amount=order.total)
        payment.process()
        messages.success(request, 'Your payment was successful.')
    except Exception as e:
        messages.warning(request, 'There was a problem with your payment.')
    return redirect('checkout_success')


# search view
def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(name__icontains=q)
        ctx = {'query': q, 'products': products}
        return render(request, 'shop/search.html', ctx)
    else:
        return redirect('all_products')
    
# category view
def all_categories(request):
    categories = Category.objects.all()
    ctx = {'categories': categories}
    return render(request, 'shop/categories.html', ctx)

def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    ctx = {'category': category, 'products': products}
    return render(request, 'shop/category.html', ctx)


def update_cart_counter(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart_count = cart.items.count()
        # save cart count to cookie
        request.session['cart_count'] = cart_count
    else:
        cart_count = 0
    return cart_count

