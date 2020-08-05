"""This file processes data recovery and inserting into tables of our data base"""
import requests
from .models import Product, Category
from django.db import DatabaseError, transaction


# TODO : requête pour catégorie et produit
# pour créer une catégorie utiliser la ligne suivante : petit_dej = Category.objects.create(category_name='petit déjeuner', url_category='https://petit_dej_au_lit.com')
# pour créer un produit utiliser la ligne suivante : nutella = Product.objects.create(product_name='nutella', nutriscore='a', fat=1, saturated_fat=1, sugars=1, salt=1, image_url='https://fake_url.com', product_url='https://fake_url_too.com')
# une fois la catégorie et le ou les produits créé, utiliser la ligne suivante : petit_dej.products.add(nutella)
# pour enregistrer un favoris :


class OpenFoodFact:
    def __init__(
        self,
        url_categories="https://fr.openfoodfacts.org/categories.json",
        number_min_food_by_category=10,
    ):
        self.url_categories = url_categories
        self.number_min_food_by_category = number_min_food_by_category

    def retrieve_all_category_name_from_open_food_facts_api(self):
        """
        This function return a list of category's name of food from open food fact api
        :return list_of_new_category of food:
        """
        response = requests.get(self.url_categories)
        print("Response : ", response)

        if response.status_code == 200:
            list_of_category = response.json().get("tags", "any data")
            print("list_of_category : ", list_of_category)

            if list_of_category:

                for category in list_of_category:
                    print("category : ", category)
                    category_db, created = Category.objects.get_or_create(
                        url_category=category.get("url"),
                        defaults={"category_name": category.get("name")},
                    )

                return 201

            else:
                return "any data found"

        return response.error, response.status_code

    # TODO :
    # 1. pour chaque category enregistré dans la base de donné trouvez les produits
    # 2. enregistrer le produit
    # 3. vérifier la catégorie est situé à quel place dans la hyerarchie du produit et attribuer une note
    # 4. enregistrer la relation entre produit et catégorie ainsi que la note (nécessite de réécrire le model pour la table de liaison product_catégorie afin d'ajouter affinity_note)
    # 5. écrire un algorithme pour la recherche des substituts qui prend en compte à la fois si le nutriscore est meilleur mais aussi si l'afinity note des catégories se correspondent)
    # list_of_category = Category.objects.all().values()
    # current category is an instance of list_category from the loop
    def give_a_hyerarchi_score_to_category_of_product(
        self,
        food,
        current_category
    ):
        """
        return a list of category + score for a product
        """
        categories = food.get('categories').split(', ')
        print('categories from give hyerarchie score : ', categories)
        hyerarchi_score = 1
        for cat in categories:
            print('CAT : ', cat)

            if cat.lower() == current_category.category_name.lower():
                return hyerarchi_score

            hyerarchi_score += 1

        return 0  # 0 == error

    def retrieve_food_with_url_category(self, current_category):
        """
        :param url_category:
        :param id_category:
        :return:
        """
        list_of_food_by_category = []
        num_page = 1
        while len(list_of_food_by_category) <= self.number_min_food_by_category:
            response = requests.get(
                current_category.url_category + "/" + str(num_page) + ".json"
            )
            print("RESPONSE FOR FOOD : ", response)
            list_of_food = response.json().get("products")
            print("list of food : ", list_of_food)
            num_page += 1
            print("number of page : ", num_page)
            print("coucou")

            if list_of_food is None:
                break

            for food in list_of_food:
                print("===============================================")
                print("product_name : ", food.get("product_name"))
                print("nutriscore : ", food.get("nutriscore_grade"))
                print("url : ", food.get("url"))
                print("fat : ", food.get("nutriments").get("fat", 0))
                print(
                    "saturated_fat : ", food.get("nutriments").get("saturated_fat", 0)
                )
                print("sugars : ", food.get("nutriments").get("sugars", 0))
                print("salt : ", food.get("nutriments").get("salt", 0))
                print("image_url : ", food.get("image_url"))
                print("categories : ", food.get("categories"))
                print("===============================================")
                if (
                    food.get("product_name")
                    and food.get("nutriscore_grade")
                    and food.get("url")
                    and food.get("image_url")
                    # and id_category
                ):
                    print("condition")
                    list_of_food_by_category.append(food.get("product_name"))

                    product, created = Product.objects.get_or_create(
                        product_name=food.get("product_name"),
                        defaults={
                            "nutriscore": food.get("nutriscore_grade"),
                            "fat": food.get("nutriments").get("fat", 0),
                            "saturated_fat": food.get("nutriments").get(
                                "saturated_fat", 0
                            ),
                            "sugars": food.get("nutriments").get("sugars", 0),
                            "salt": food.get("nutriments").get("salt", 0),
                            "image_url": food.get("image_url"),
                            "product_url": food.get("url"),
                        },
                    )
                    hyerarchie_score = self.give_a_hyerarchi_score_to_category_of_product(
                        food, current_category)
                    current_category.products.add(
                        product,
                        through_defaults={
                           'hyerarchie_score': hyerarchie_score
                        }
                    )

            print("size_of_list_of_food_by_category : ", len(list_of_food_by_category))

            if len(list_of_food) < 20:
                break

        if list_of_food_by_category == []:
            return "any food contain in this category"

        return list_of_food_by_category

    @staticmethod
    def filter_category_by_interest(
        list_of_new_category, list_of_keywords
    ):  # idea : do a forbidden list !
        """
        :param list_of_new_category:
        :param list_of_keywords:
        :return list_of_interesting_category:
        """
        list_of_interesting_category = []

        for new_category in list_of_new_category:
            category_name = new_category.get("category_name")

            for keywords in list_of_keywords:

                if keywords in category_name:

                    if "viande" not in category_name or "lait" not in category_name:
                        list_of_interesting_category.append(new_category)
                        break

        return list_of_interesting_category
