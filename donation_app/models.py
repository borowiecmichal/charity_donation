from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    TYPE_CHOICES = (
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna'),
    )

    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    category = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    address = models.TextField()
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.TextField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_DEFAULT)
