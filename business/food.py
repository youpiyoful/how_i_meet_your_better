"""
file about class food who deliver method about himyb functionalities
like search a food substitute
"""
from .models import Category, Product
from django.core.exceptions import ObjectDoesNotExist


class Food:
    """
    class of food than deliver all the method
    about food and substitute
    """
    def __init__(self, food):
        self.food = food

    def search_food_and_categories_by_product_name(self):
        """
        search food in the db with the name of food 
        of the instance Food
        : return the product and associated categories
        """
        try:
            product = Product.objects.get(product_name=self.food)
            categories = product.category_set.all()
            print('COUCOU PRODUCT : ', categories)

        except ObjectDoesNotExist:
            print('Either the product or categories of product doesn\'t exist')
            return 'product not found'

        list_of_category = []

        for cat in categories:
            category_hyerarchie = Category.objects.get(
                id=cat.id
            ).categoriesproducts_set.all().filter(
                category_id=cat.id,
                product_id=product.id
            )[0].hyerarchie_score
            category = {
                "category_id": cat.id,
                "category_name": cat.category_name,
                "url_category": cat.url_category,
                "category_hyerarchie": category_hyerarchie
            }

            list_of_category.append(category)

        complete_product = {
            'product': {
                'product_id': product.id,
                'product_name': product.product_name,
                'product_url': product.product_url,
                'image_url': product.image_url,
                'nutriscore': product.nutriscore,
                'salt': product.salt,
                'sugars': product.sugars,
                'fat': product.fat,
                'saturated_fat': product.saturated_fat,
            },
            'categories': list_of_category
        }

        print('complete_product : ', complete_product)
        return complete_product

    def substitute_food_by_foods_with_best_nutriscore(self, complete_product): 
        """
        for a food find many foods than have a best nutriscore
        : return list of substitute
        """
        current_product_id = complete_product.get('product_id')
        # categories = complete_product.get('categories')
        nutriscore_of_current_product = complete_product.get(
            'product').get('nutriscore')

        # Retrieve categories of product choice by the user
        # order by hyerarchie_categorie.
        list_of_cat_order_by_hyerarchie_score = Product.objects.get(
            id=current_product_id
        ).categoriesproducts_set.all().order_by(
            'hyerarchie_score')
        # Retrieve the unique more precise category in the list.
        more_precise_cat = list_of_cat_order_by_hyerarchie_score[
            len(list_of_cat_order_by_hyerarchie_score):][0].id

        # The list of substitutes in the same category with a
        # better nutriscore emerges.
        queryset_list_of_substitute = Category.objects.get(
            id=more_precise_cat
        ).products.all().filter(
            nutriscore__lte=nutriscore_of_current_product
        ).exclude(id=current_product_id).order_by('nutriscore')

        list_of_substitute = [
            substitute for substitute in queryset_list_of_substitute
        ]

        if len(list_of_substitute) > 6:
            # return the 6 best substitute in the list
            return list_of_substitute[:6]

        if list_of_substitute:
            return list_of_substitute

        return 'any substitute found'

        # 1. sélectionner la catégorie du produit choisie par l' utilisateur possédant 
        # le hierarchie_score le plus petit et donc la catégorie du produit la plus général
        # sauvegarder également la liste de tout les catégories du produit source.
        # 2. on veut récupérer tous les produits de cette catégorie.
        # 3. Pour chaque produit de cette catégorie on veut récupérer ceux qui on au minimum 
        # 3 catégories en commun avec le produit source. Ce qui veut dire que l'on doit connaître les 
        # catégories du produit source. retour à l'étape 1
        # 4 faire une boucle et comparer les produits un a un avant de les sauvegarder.