"""this file is the models for the relation mapping"""
from django.db import models


class Product(models.Model):
    """
    Product of categories : name, nutriscore, image...
    """

    product_name = models.CharField(max_length=300, unique=True)
    nutriscore = models.CharField(max_length=1, null=False)
    image_url = models.URLField(verbose_name="Url de l'image du produit", null=True)
    product_url = models.URLField(
        verbose_name="Url du produit",
        unique=True,
        null=False,
        default="aucune url trouvé",
    )
    fat = models.DecimalField(max_digits=12, decimal_places=8)
    saturated_fat = models.DecimalField(max_digits=12, decimal_places=8)
    sugars = models.DecimalField(max_digits=12, decimal_places=8)
    salt = models.DecimalField(max_digits=12, decimal_places=8)
    # openfoodfacts_link = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name

    class Meta:
        """config of table with order by product_name
        and rename the name"""
        verbose_name = "Produit"
        ordering = ["product_name"]


class Category(models.Model):
    """
    Category of product : name, url_category
    """

    category_name = models.CharField(max_length=300)
    products = models.ManyToManyField(Product, through="CategoriesProducts")
    url_category = models.URLField(
        verbose_name="Url de la categorie", unique=True, null=False, max_length=600
    )

    def __str__(self):
        return self.category_name

    class Meta:
        """
        configure the table with verbose name 
        and ordering by category_name
        """
        verbose_name = "Catégorie"
        ordering = ["category_name"]


class CategoriesProducts(models.Model):
    """
    create that table for add the field hyerarchie_score
    that determine if a category is more or less precise.
    The lower the score, the more general the category
    and vice versa.
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    hyerarchie_score = models.IntegerField(default=0)

    class Meta:
        """force the table name"""
        db_table = "business_categories_products"
