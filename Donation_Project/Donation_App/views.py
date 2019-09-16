from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import Donation_List, DonationType
from orders.models import Order


# Create your views here.


def start_page(request):
    return render(request, 'index.html')


def user_management(request):
    users = User.objects.all()
    return render(request, 'UserManagement.html', {'users': users})


def add_user(request):
    if request.method == 'POST':
        if 'save' in request.POST:
            if request.POST.get('firstname') and request.POST.get('lastname') and request.POST.get(
                    'email') and request.POST.get('password') and request.POST.get('role'):
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                email = request.POST.get('email')
                password = request.POST.get('password')
                role_text = request.POST.get('role')
                role_num = 1
                if role_text == 'user':
                    role_num = 0
                user = User.objects.create_user(username=email, email=email, password=password, first_name=firstname,
                                                last_name=lastname, is_staff=role_num)
                return redirect('Donation_App:user_management')
            else:
                return render(request, 'add_user.html')
        else:
            return redirect('Donation_App:user_management')
    else:
        return render(request, 'add_user.html')


def edit_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        if 'save' in request.POST:
            if request.POST.get('firstname') and request.POST.get('lastname') and request.POST.get(
                    'email') and request.POST.get('role'):
                user.first_name = request.POST.get('firstname')
                user.last_name = request.POST.get('lastname')
                user.email = request.POST.get('email')
                user.username = request.POST.get('email')
                if request.POST.get('password') != '':
                    user.set_password(request.POST.get('password'))
                role_text = request.POST.get('role')
                role_num = 1
                if role_text == 'user':
                    role_num = 0
                user.is_staff = role_num
                user.save()
                return redirect('Donation_App:user_management')
            else:
                return render(request, 'edit_user.html', {'user': user})
        else:
            return redirect('Donation_App:user_management')
    else:
        return render(request, 'edit_user.html', {'user': user})


def delete_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.delete()
    return redirect('Donation_App:user_management')


def donation_management(request):
    donations = Donation_List.objects.all()
    return render(request, 'DonationManagement.html', {'donations': donations})


def user_authentication(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        request.session.set_expiry(60 * 5)
        return redirect(start_page)
    else:
        return render(request, 'login_page.html')


def user_logout(request):
    logout(request)
    request.session.clear_expired()
    return render(request, 'logout_page.html')


def personal_information(request):
    if request.method == 'POST':
        if 'continue' in request.POST:
            if request.POST.get('firstname') and request.POST.get('lastname') and request.POST.get(
                'cma') and request.POST.get('email'):
                request.session['firstname'] = request.POST.get('firstname')
                request.session['lastname'] = request.POST.get('lastname')
                request.session['cma'] = request.POST.get('cma')
                request.session['phone'] = request.POST.get('phone')
                request.session['email'] = request.POST.get('email')
                request.session['addr1'] = request.POST.get('addr1')
                request.session['addr2'] = request.POST.get('addr2')
                request.session['city'] = request.POST.get('city')
                request.session['state'] = request.POST.get('state')
                request.session['postal'] = request.POST.get('postal')
                request.session['country'] = request.POST.get('country')
                request.session['urb'] = request.POST.get('urb')
                return redirect('Donation_App:gift')
            else:
                return render(request, 'personal_information.html')
        else:
            return redirect('Donation_App:userview')
    else:
        if request.user.is_authenticated:
            donation = Order.objects.filter(email=request.user.email).order_by('-created')
            print(donation.count())
            if donation.count() == 0:
                donation = False
            else:
                donation = donation[0]
            return render(request, 'personal_information.html', {'donation': donation})
        else:
            return render(request, 'personal_information.html')

def user_view(request):
    if request.POST:
        return redirect('Donation_App:personal_information')
    else:
        if request.user.is_authenticated:
            full_name = request.user.first_name + ' ' + request.user.last_name
            donationList = Donation_List.objects.filter(name=full_name)
            if donationList.count() == 0:
                donationList = False
            return render(request, 'UserView.html', {'donationList': donationList})
        else:
            return render(request, 'UserView.html')


def gift(request):
    donation_types = DonationType.objects.all()
    if request.method == 'POST':
        if 'continue' in request.POST:
            donations = []
            for dtypes in donation_types:
                if request.POST.get(str(dtypes.pk)):
                    request.session['pk' + str(dtypes.pk)] = request.POST.get(str(dtypes.pk))
                    donations.append(dtypes)
            if len(donations) == 0:
                return redirect('Donation_App:gift')
            else:
                request.session['items_to_add'] = donations
                request.session.modified = True
                return redirect('cart:cart_add')
        else:
            return redirect('Donation_App:userview')
    else:
        return render(request, 'gift.html', {'donation_types': donation_types})


