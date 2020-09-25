"""
file about class food who deliver method about himyb functionalities
like search a food substitute
"""
from business.models import Category, Product
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import string


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
            print("COUCOU PRODUCT : ", categories)

        except ObjectDoesNotExist:
            print("Either the product or categories of product doesn't exist")
            return "product not found"

        list_of_category = []

        for cat in categories:
            category_hyerarchie = (
                Category.objects.get(id=cat.id)
                .categoriesproducts_set.all()
                .filter(category_id=cat.id, product_id=product.id)[0]
                .hyerarchie_score
            )
            category = {
                "category_id": cat.id,
                "category_name": cat.category_name,
                "url_category": cat.url_category,
                "category_hyerarchie": category_hyerarchie,
            }

            list_of_category.append(category)

        complete_product = {
            "product": {
                "product_id": product.id,
                "product_name": product.product_name,
                "product_url": product.product_url,
                "image_url": product.image_url,
                "nutriscore": product.nutriscore,
                "salt": product.salt,
                "sugars": product.sugars,
                "fat": product.fat,
                "saturated_fat": product.saturated_fat,
            },
            "categories": list_of_category,
        }

        print("complete_product : ", complete_product)
        return complete_product

    def substitute_food_by_foods_with_best_nutriscore(self, complete_product):
        """
        for a food find many foods than have a best nutriscore
        : return list of substitute
        """
        print("=============================================")
        print("complete_product : ", complete_product)
        current_product_id = complete_product.get("product").get("product_id")
        print("current_product_id : ", current_product_id)
        nutriscore_of_current_product = complete_product.get("product").get(
            "nutriscore"
        )
        print("nutriscore_of_current_product : ", nutriscore_of_current_product)

        # Retrieve categories of product choice by the user
        # order by hyerarchie_categorie.
        list_of_cat_order_by_hyerarchie_score = (
            Product.objects.get(id=current_product_id)
            .categoriesproducts_set.all()
            .order_by("hyerarchie_score")
        )
        print(
            "list_of_cat_order_by_hyerarchie_score : ",
            list_of_cat_order_by_hyerarchie_score,
        )
        # Retrieve the unique more precise category in the list.
        if list_of_cat_order_by_hyerarchie_score:
            
            # choose the category_id of the first element of the list
            if len(list_of_cat_order_by_hyerarchie_score) > 1:
                more_precise_cat = list_of_cat_order_by_hyerarchie_score[
                    len(list_of_cat_order_by_hyerarchie_score) - 1 :
                ][0].category_id

            else:
                more_precise_cat = list_of_cat_order_by_hyerarchie_score[0].category_id

            print("more_precise_cat : ", more_precise_cat)
            # The list of substitutes in the same category with a
            # better nutriscore emerges.
            print("product test : ", Product.objects.all()[0].id)
            print("category not match : ", Category.objects.get(id=more_precise_cat))
            queryset_list_of_substitute = (
                Category.objects.get(id=more_precise_cat)
                .products.all()
                .filter(nutriscore__lte=nutriscore_of_current_product)
                .exclude(id=current_product_id)
                .order_by("nutriscore")
                .all()
                .values()
            )
            print("queryset_list_of_substitute : ", queryset_list_of_substitute)

            list_of_substitute = [
                substitute for substitute in queryset_list_of_substitute
            ]
            print("list_of_substitute : ", list_of_substitute)
            print("nutriscore of current product : ", nutriscore_of_current_product)
            commune_cat = Category.objects.get(id=more_precise_cat).category_name
            if len(list_of_substitute) > 6:
                # return the 6 best substitute in the list
                return list_of_substitute[:6], commune_cat

            if list_of_substitute:
                return list_of_substitute, commune_cat

        return "this product have the best nutriscore", "category commune"

        def record_a_favorite_substitute(self):
            """
            This function take a substitute and his product
            and record him in favorite table
            """
            pass

        # 1. sélectionner la catégorie du produit choisie par l' utilisateur possédant
        # le hierarchie_score le plus petit et donc la catégorie du produit la plus général
        # sauvegarder également la liste de tout les catégories du produit source.
        # 2. on veut récupérer tous les produits de cette catégorie.
        # 3. Pour chaque produit de cette catégorie on veut récupérer ceux qui on au minimum
        # 3 catégories en commun avec le produit source. Ce qui veut dire que l'on doit connaître les
        # catégories du produit source. retour à l'étape 1
        # 4 faire une boucle et comparer les produits un a un avant de les sauvegarder.
