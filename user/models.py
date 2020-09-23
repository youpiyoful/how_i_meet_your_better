"""
extention of user model
"""
from django.db import models
from django.contrib.auth.models import User
from business.models import Product


class Favorite(models.Model):
    substitute = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='%(class)s_substitute')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='%(class)s_product')

    def __str__(self):
        return ("Substitut : " + str(self.substitute)
                + " / Produit : " + str(self.product))

    class Meta:
        verbose_name = "Favoris"
        verbose_name_plural = "Favoris"
        ordering = ['product']


class PurBeurreUser(models.Model):
    """
    extend user model for add favoris product
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Favorite)

    def __str__(self):
        username = self.user.first_name + ' ' + self.user.last_name
        return f"Compte de {username}"

    # @property
    # def full_name(self):
    #     "returns the person's full name."
    #     return '%s %s' % (self.first_name, self.last_name)
