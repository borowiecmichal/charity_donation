from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from donation_app.models import Donation, Institution, MyUser, Category


class LandingPageView(View):
    def get(self, request):
        foundations = Institution.objects.filter(type=1)
        foundations_paginator = Paginator(foundations, 5)
        ngos = Institution.objects.filter(type=2)
        ngos_paginator = Paginator(ngos, 5)
        local_foundings = Institution.objects.filter(type=3)
        local_foundings_paginator = Paginator(local_foundings, 5)
        ctx = {
            'num_of_given_bags': Donation.objects.aggregate(Sum('quantity'))['quantity__sum'],
            'num_of_supported_orgs': Donation.objects.all().distinct('institution').count(),
            'foundations': foundations_paginator.get_page(1),
            'ngos': ngos,
            'locals': local_foundings,
        }
        return render(request, 'index.html', ctx)


class AddDonationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            ctx={
                'categories':Category.objects.all(),
                'institutions': Institution.objects.all()
            }
            return render(request, 'form.html', ctx)
        else:
            return redirect(reverse('login'))


class LoginUserView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect(reverse('landing-view'))
        else:
            return redirect(reverse('register'))


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('landing-view'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:

            try:
                validate_password(password)
                MyUser.objects.get(email=email)
                return render(request, 'register.html', {'err': 'Email już jest zajęty'})
            except ValidationError:
                return render(request, 'register.html', {'err': 'Hasło nie spełnia wymagań'})
            except:
                user = MyUser.objects.create_user(email=email, password=password, first_name=name, last_name=surname)
                return redirect(reverse('login'))
