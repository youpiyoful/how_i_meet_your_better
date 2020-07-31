"""This file processes data recovery and inserting into tables of our data base"""
import requests
from .models import Product, Category

# TODO : requête pour catégorie et produit
# pour créer une catégorie utiliser la ligne suivante : petit_dej = Category.objects.create(category_name='petit déjeuner', url_category='https://petit_dej_au_lit.com')
# pour créer un produit utiliser la ligne suivante : nutella = Product.objects.create(product_name='nutella', nutriscore='a', fat=1, saturated_fat=1, sugars=1, salt=1, image_url='https://fake_url.com', product_url='https://fake_url_too.com')
# une fois la catégorie et le ou les produits créé, utiliser la ligne suivante : petit_dej.products.add(nutella)
# pour enregistrer un favoris : 


class OpenFoodFact:
    def __init__(self, url_categories='https://fr.openfoodfacts.org/categories.json', number_min_food_by_category=10):
        self.url_categories = url_categories
        self.number_min_food_by_category = number_min_food_by_category

    def retrieve_all_category_name_from_open_food_facts_api(self):
        """
        This function return a list of category's name of food from open food fact api
        :return list_of_new_category of food:
        """
        response = requests.get(self.url_categories)
        list_of_category = response.json().get('tags')
        list_of_new_category = []

        for category in list_of_category:
            new_category = {
                'category_name': category.get('name'),
                'url_category': category.get('url')
            }
            Category.objects.create(
                category_name=new_category.get('category_name'),
                url_category=new_category.get('url_category')
            )
            list_of_new_category.append(new_category)

        return list_of_new_category

# TODO : 
# 1. pour chaque category enregistré dans la base de donné trouvez les produits
# 2. enregistrer le produit
# 3. vérifier la catégorie est situé à quel place dans la hyerarchie du produit et attribuer une note
# 4. enregistrer la relation entre produit et catégorie ainsi que la note (nécessite de réécrire le model pour la table de liaison product_catégorie afin d'ajouter affinity_note)
# 5. écrire un algorithme pour la recherche des substituts qui prend en compte à la fois si le nutriscore est meilleur mais aussi si l'afinity note des catégories se correspondent) 

    def retrieve_food_with_url_category(self, url_category, id_category):
        """
        :param url_category:
        :param id_category:
        :return:
        """
        list_of_food_by_category = []
        num_page = 1

        while len(list_of_food_by_category) <= self.number_min_food_by_category:
            response = requests.get(url_category + '/' + str(num_page) + '.json')
            list_of_food = response.json().get('products')
            print('list of food : ', list_of_food)
            num_page += 1
            print('number of page : ', num_page)

            if len(list_of_food) == 0:
                break

            for food in list_of_food:

                if food.get('product_name') and food.get('generic_name') and food.get('url') and food.get(
                        'nutriscore_score') and id_category:
                    new_food = {
                        'product_name': food.get('product_name'),
                        'generic_name': food.get('generic_name'),
                        'stores_tags': food.get('stores_tags'),
                        'url': food.get('url'),
                        'nutrition_grades': food.get('nutriscore_score'),
                        'id_category': id_category
                    }
                    list_of_food_by_category.append(new_food)
            print(len(list_of_food_by_category))

            if len(list_of_food) < 20:
                break

        return list_of_food_by_category

    @staticmethod
    def filter_category_by_interest(list_of_new_category, list_of_keywords):  # idea : do a forbidden list !
        """
        :param list_of_new_category:
        :param list_of_keywords:
        :return list_of_interesting_category:
        """
        list_of_interesting_category = []

        for new_category in list_of_new_category:
            category_name = new_category.get('category_name')

            for keywords in list_of_keywords:

                if keywords in category_name:

                    if 'viande' not in category_name or 'lait' not in category_name:
                        list_of_interesting_category.append(new_category)
                        break

        return list_of_interesting_category