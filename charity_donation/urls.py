"""charity_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from donation_app.views import LandingPageView, AddDonationView, LoginUserView, RegisterView, LogoutUserView, \
    UserProfileView, TakeDonationView, UpdateProfile, ConfirmFormView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPageView.as_view(), name='landing-view'),
    path('donate/', AddDonationView.as_view(), name='donate'),
    path('donate-confirmed/', ConfirmFormView.as_view(), name='form-confirmation'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('myProfile/', UserProfileView.as_view(), name='user-profile'),
    path('myProfile/edit/', UpdateProfile.as_view(), name='edit-profile'),
    path('take-donation/<int:id>', TakeDonationView.as_view(), name='take-donation'),
]
