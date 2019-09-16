from django.shortcuts import render, redirect, get_object_or_404
from Donation_App.models import DonationType
from . cart import Cart


def cart_add(request):
    cart = Cart(request)
    for donation_pk in request.session.get('items_to_add'):
        donation = get_object_or_404(DonationType, pk=donation_pk.pk)
        cart.add_cart(donation_type=donation,
                      price=request.session.get('pk' + str(donation_pk.pk)))
    return redirect('cart:cart_detail')


def cart_remove(request, donation_pk):
    cart = Cart(request)
    donation = get_object_or_404(DonationType, pk=donation_pk)
    cart.remove_from_cart(donation)
    return redirect('cart:cart_detail')


def empty_cart(request):
    cart = Cart(request)
    cart.clear_cart()
    return redirect('Donation_App:userview')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

