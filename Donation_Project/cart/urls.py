from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/$', views.cart_add, name='cart_add'),
    url(r'^empty_cart/$', views.empty_cart, name='empty_cart'),
    url(r'^remove/(?P<donation_pk>\d+)/$', views.cart_remove, name='cart_remove'),
]
