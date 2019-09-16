from decimal import Decimal
from django.conf import settings
from Donation_App.models import DonationType


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        donation_pks = self.cart.keys()
        donation_types = DonationType.objects.filter(pk__in=donation_pks)
        for donation_type in donation_types:
            self.cart[str(donation_type.pk)]['donation_type'] = donation_type

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_quantity(self):
        total_quantity = sum(Decimal(item['quantity']) for item in self.cart.values())
        return total_quantity

    def add_cart(self, donation_type, price):
        donation_pk = str(donation_type.pk)
        if donation_pk not in self.cart:
            self.cart[donation_pk] = {'quantity': 1,
                                      'price': Decimal(price)}
        else:
            self.cart[donation_pk]['quantity'] += 1
            self.cart[donation_pk]['price'] += Decimal(price)
        self.save_cart()

    def save_cart(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove_from_cart(self, donation_type):
        donation_pk = str(donation_type.pk)
        if donation_pk in self.cart:
            del self.cart[donation_pk]
            self.save_cart()

    def clear_cart(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())
