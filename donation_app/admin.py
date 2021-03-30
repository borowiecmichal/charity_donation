from django.contrib import admin

# Register your models here.
from donation_app.models import MyUser, Institution


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    pass