from django.db import models


class Product(models.Model):
    """
    Product of categories : name, nutriscore, image...
    """
    product_name = models.CharField(max_length=100, unique=True)
    nutriscore = models.CharField(max_length=1, null=False)
    image_url = models.URLField(
        verbose_name="Url de l'image du produit",
        null=True)
    product_url = models.URLField(verbose_name="Url du produit", unique=True)
    fat = models.IntegerField()
    saturated_fat = models.IntegerField()
    sugars = models.IntegerField()
    salt = models.IntegerField()
    openfoodfacts_link = models.CharField(max_length=100)
    # TODO dans openfoodfacts on trouve ces informations à ce chemin
    # nutriments.get('salt'), nutriments.get('sugars') etc...

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Produit"
        ordering = ['product_name']


class Category(models.Model):
    """
    Category of product : name
    """
    category_name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='categories')
    url_category = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Catégorie"
        ordering = ['category_name']
