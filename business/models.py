from django.db import models


class Product(models.Model):
    """
    Product of categories : name, nutriscore, image...
    """
    product_name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=100)
    image = models.CharField(max_length=150)
    fat = models.IntegerField()
    saturated_fat = models.IntegerField()
    sugars = models.IntegerField()
    salt = models.IntegerField()
    openfoodfacts_link = models.CharField(max_length=100)
    # TODO dans openfoodfacts on trouve ces informations à ce chemin
    # nutriments.get('salt'), nutriments.get('sugars') etc...


class Category(models.Model):
    """
    Category of product : name
    """
    category_name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='categories')
