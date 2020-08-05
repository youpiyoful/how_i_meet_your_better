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
            # categories = Category.objects.filter(products=product.id)# order_by(category_hyerarchie)
            print('COUCOU PRODUCT : ', categories)

        except ObjectDoesNotExist:
            print('Either the product or categories of product doesn\'t exist')
            return 'product not found'

        list_of_category = []

        for cat in categories:
            category = {
                "category_id": cat.id,
                "category_name": cat.category_name,
                "url_category": cat.url_category,
                "category_hyerarchie": ""
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
        categories = complete_product.get('categories')
        nutriscore = complete_product.get('product').get('nutriscore')
        substitute = Category.objects.filter('')
