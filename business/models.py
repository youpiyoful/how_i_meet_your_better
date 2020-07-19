from django.db import models
from user.models import PurBeurreUser


class Product(models.Model):
    """
    Product of categories : name, nutriscore, image...
    """
    product_name = models.CharField()
    nutriscore = models.CharField()
    image = models.ImageField()
    categories = models.ManyToManyField(Category, related_name='products')
    user = models.ManyToManyField(
        PurBeurreUser,
        related_name='favoris_product'
    )
    fat = models.IntegerField()
    saturated_fat = models.IntegerField()
    sugars = models.IntegerField()
    salt = models.IntegerField()
    openfoodfacts_link = models.CharField()
    # TODO dans openfoodfacts on trouve ces informations à ce chemin
    # nutriments.get('salt'), nutriments.get('sugars') etc...


class Category(models.Model):
    """
    Category of product : name
    """
    category_name = models.CharField()
    # bind_category = models.ManyToManyField("self")
    products = models.ManyToManyField(Product, related_name='categories')
