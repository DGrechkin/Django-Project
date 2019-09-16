from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start_page),
    url(r'UserManagement/$', views.user_management, name='user_management'),
    url(r'add_user/$', views.add_user, name='add_user'),
    url(r'edit/(?P<user_pk>\d+)/$', views.edit_user, name='edit_user'),
    url(r'delete/(?P<user_pk>\d+)/$', views.delete_user, name='delete_user'),
    url(r'DonationManagement/$', views.donation_management, name='donation_management'),
    url(r'userview/$', views.user_view, name='userview'),
    url(r'personal_information/$', views.personal_information, name='personal_information'),
    url(r'gift/$', views.gift, name='gift'),
]
