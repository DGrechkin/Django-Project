from django.shortcuts import render, redirect
from . models import Order, OrderItem
from cart.cart import Cart
from Donation_App.models import Donation_List
from django.core.mail import send_mail
from decimal import Decimal


# Create your views here.


def order_create(request):
    cart = Cart(request)
    order = Order(first_name=request.session['firstname'], last_name=request.session['lastname'],
                  email=request.session['email'], cma=int(request.session['cma']),
                  phone=request.session['phone'], address1=request.session['addr1'],
                  address2=request.session['addr2'], city=request.session['city'],
                  state=request.session['state'], postal=request.session['postal'],
                  country=request.session['country'], urbanization=request.session['urb'])
    if request.method == 'POST':
        if 'checkout' in request.POST:
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         donation_type=item['donation_type'],
                                         total_price=item['price'],
                                         quantity=item['quantity'])

                Donation_List.objects.create(name=request.session['firstname'] + ' ' + request.session['lastname'],
                                             amount=item['price'],
                                             donationType=item['donation_type'].name)
            cart.clear_cart()
            send_mail(
                'Donation',
                'Thank you very much for your donation',
                'dmitriygrechkin1992@gmail.com',
                [request.session['email']],
                fail_silently=False,
            )
            return render(request, 'created.html', {'order': order})
        else:
            return redirect('Donation_App:userview')
    else:
        return render(request, 'create.html', {'cart': cart, 'order': order})
