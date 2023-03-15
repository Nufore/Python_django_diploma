from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app_store.models import Product
from app_store.forms import UpdateQuantityForm
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('app_store:product_detail', pk=product_id)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('app_store:cart')


@require_POST
def cart_update_plus(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # form = UpdateQuantityForm(request.POST)
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('app_store:cart')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
