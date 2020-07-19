"""
extention of user model
"""
from django.db import models
from django.contrib.auth.models import User
from business.models import Product


class PurBeurreUser(models.Model):
    """
    extend user model for add favoris product
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favoris_product = models.ManyToManyField(Product, related_name="user")