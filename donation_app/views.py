import datetime
import json

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView

from donation_app.forms import UserCreateForm, LoginForm, UpdateUserForm, DonationForm
from donation_app.models import Donation, Institution, MyUser, Category


class LandingPageView(View):
    def get(self, request):
        foundations = Institution.objects.filter(type=1)
        foundations_paginator = Paginator(foundations, 2)
        ngos = Institution.objects.filter(type=2)
        ngos_paginator = Paginator(ngos, 5)
        local_foundings = Institution.objects.filter(type=3)
        local_foundings_paginator = Paginator(local_foundings, 5)

        if request.GET:
            a = request.GET.get('foundation_page')
            print(a)
            lista = foundations_paginator.get_page(a)
            print(lista)
            slownik = {}
            i = 0
            for item in lista:
                slownik[f'el{i}'] = {
                    'name': item.name,
                    'description': item.description,
                    'categories': item.category_list_string
                }
                i += 1

            print(lista.has_previous(), lista.has_next())
            print(slownik)
            slownik['has_previous'] = lista.has_previous()
            slownik['has_next'] = lista.has_next()
            return JsonResponse(slownik)

        else:

            ctx = {
                'num_of_given_bags': Donation.objects.aggregate(Sum('quantity'))['quantity__sum'],
                'num_of_supported_orgs': Donation.objects.all().distinct('institution').count(),
                'foundations': foundations_paginator.get_page(1),
                'foundation_number_of_pages_range': foundations_paginator.page_range,
                'ngos': ngos,
                'locals': local_foundings,
            }
            return render(request, 'index.html', ctx)


class AddDonationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = DonationForm()
            ctx = {
                'form': form,
            }
            return render(request, 'form2.html', ctx)
        else:
            return redirect(reverse('login'))

    def post(self, request):
        if request.is_ajax:
            form = DonationForm(request.POST)
            print(form.errors)
            print(form.is_valid())
            if form.is_valid():
                donation = Donation.objects.create(quantity=form.cleaned_data['quantity'],
                                                   institution=form.cleaned_data['institution'],
                                                   address=form.cleaned_data['address'],
                                                   phone_number=form.cleaned_data['phone_number'],
                                                   city=form.cleaned_data['city'],
                                                   zip_code=form.cleaned_data['zip_code'],
                                                   pick_up_date=form.cleaned_data['pick_up_date'],
                                                   pick_up_time=form.cleaned_data['pick_up_time'],
                                                   pick_up_comment=form.cleaned_data['pick_up_comment'],
                                                   user=request.user
                                                   )

                donation.categories.add(*form.cleaned_data['categories'])
                return JsonResponse({'url_success': reverse('landing-view')})
            else:

                errors = {
                    key: errors for key, errors in form.errors
                }
                return JsonResponse({'url_success': reverse('landing-view')}, status=400)


# class AddDonationView(FormView):
#     form_class = DonationForm
#     template_name = 'form2.html'
#
#     def form_valid(self, form):
#         if self.request.is_ajax and self.request == 'POST':
#             form_data_dict = self.request.POST
#             print(form_data_dict)
#             donation = Donation.objects.create(quantity=form_data_dict['bags'],
#                                                institution_id=form_data_dict['organization'],
#                                                address=form_data_dict['address'],
#                                                phone_number=form_data_dict['phone'],
#                                                city=form_data_dict['city'],
#                                                zip_code=form_data_dict['postcode'],
#                                                pick_up_date=datetime.datetime.strptime(form_data_dict['data'],
#                                                                                        '%Y-%m-%d').date(),
#                                                pick_up_time=datetime.datetime.strptime(form_data_dict['time'],
#                                                                                        '%H:%M').time(),
#                                                pick_up_comment=form_data_dict['more_info'],
#                                                user=self.request.user
#                                                )
#             for id_category in self.request.POST['categories']:
#                 donation.categories.add(Category.objects.get(id=id_category))
#             return JsonResponse({'url_success': reverse('landing-view')})


class ConfirmFormView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('landing-view')


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('landing-view'))


class RegisterView(FormView):
    form_class = UserCreateForm
    template_name = 'register.html'
    success_url = reverse_lazy('landing-view')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        MyUser.objects.create_user(email=form.cleaned_data['email'], password=form.cleaned_data['password1'],
                                   first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
        return super().form_valid(form)


class UserProfileView(View):
    def get(self, request):
        return render(request, 'user-profile.html')


class TakeDonationView(View):
    def get(self, request, id):
        donation = Donation.objects.get(pk=id)
        if donation.is_taken:
            donation.is_taken = False
        else:
            donation.is_taken = True
        donation.save()
        return redirect(reverse('user-profile'))


class UpdateProfile(View):
    def get(self, request):
        form = UpdateUserForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

        change_password_form = PasswordChangeForm(request.user)
        return render(request, 'updateProfile.html', {'form': form, 'change_password_form': change_password_form})

    def post(self, request):
        if 'form' in request.POST:

            form = UpdateUserForm(request.POST, instance=request.user)

            if form.is_valid():
                print(request.user.email, form.cleaned_data['password'])
                if request.user.check_password(form.cleaned_data['password']):
                    # form.instance = request.user
                    form.save()

                return redirect(reverse('landing-view'))

        elif 'form2' in request.POST:
            change_password_form = PasswordChangeForm(request.user, request.POST)

            if change_password_form.is_valid():
                if change_password_form.clean_old_password():
                    user = change_password_form.save()
                    update_session_auth_hash(request, user)
                return HttpResponse('zmiana hasla dokonana')

        raise Http404
