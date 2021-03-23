from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from donation_app.models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        ctx = {
            'num_of_given_bags': Donation.objects.aggregate(Sum('quantity'))['quantity__sum'],
            'num_of_supported_orgs': Donation.objects.all().distinct('institution').count()
        }
        return render(request, 'index.html', ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginUserView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
