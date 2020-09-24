from django.test import TestCase
from .models import Product, Category
from business import open_food_facts, food
from unittest.mock import MagicMock
from decimal import *
import random
import string

# import requests


# region TEST OF CLASSES
# region mock class
class MockResponseToApi:
    """
    mock the response of api open food fact
    for category
    """

    def __init__(self, status_code, data_not_found=None):
        self.status_code = status_code
        self.data_not_found = data_not_found

        if status_code != 200:
            self.error = "the server encounter an internal error"

    def json(self):
        """
        response of api open food fact
        """
        if self.data_not_found:
            json_response = {"tags": []}

        else:
            json_response = {
                "tags": [
                    {"url": "https://fake_url.com", "name": "faux produit de test"}
                ]
            }

        return json_response


class MockResponseToApiForFood:
    """
    mock the response of open food fact 
    when we call him for retrieve food
    from an url category
    """

    def __init__(self, status_code, data_not_found=None):
        self.status_code = status_code
        self.data_not_found = data_not_found

        if status_code != 200:
            self.error = "the server encounter an internal error"

    def json(self):

        if self.data_not_found:
            json_response = {"products": []}

        else:
            json_response = {
                "products": [
                    {
                        "product_name": "nutella",
                        "nutriscore_grade": "d",
                        "url": "https://nutella.com",
                        "nutriments": {
                            "fat": 10,
                            "saturated_fat": 15,
                            "sugars": 10,
                            "salt": 0.5,
                        },
                        "image_url": "htts://nutella.jpg",
                        "categories": "Produits à tartiner, Petit-déjeuners, Produits à tartiner sucrés, Pâtes à tartiner, Pâtes à tartiner au chocolat"
                    }
                ]
            }
        return json_response


# endregion


class TestOpenFoodFacts(TestCase):
    """
    test all the method of class openFoodFacts
    than use the api openfood fact and populate the db
    """

    def setUp(self):
        """
        instanciate the obj
        create a fake category
        create a fake json food
        """
        self.open_food_fact = open_food_facts.OpenFoodFact()
        # create a fake category
        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(200))
        self.fake_cat = Category.objects.create(
            category_name="petit dej", url_category="https://petit_dej_au_lit.com"
        )
        self.json_food = {
            "categories": "Produits à tartiner, Petit-déjeuners, Produits à tartiner sucrés, Pâtes à tartiner, Pâtes à tartiner au chocolat"
        }

    def test_than_retrieve_all_category_from_open_food_fact_is_ok(self):
        """
        test than function record the category in the db
        and return status 201
        """

        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(200))
        result = (
            self.open_food_fact.retrieve_all_category_name_from_open_food_facts_api()
        )
        cat = Category.objects.all()[0]
        self.assertNumQueries(1)
        self.assertEqual(result, 201)
        self.assertEqual(cat.url_category, "https://fake_url.com")

    def test_retrieve_all_category_when_api_return_any_data(self):
        """
        test than function return 'any data found' when the api
        open food fact return nothing
        """
        open_food_facts.requests.get = MagicMock(
            return_value=MockResponseToApi(200, True)
        )
        result = (
            self.open_food_fact.retrieve_all_category_name_from_open_food_facts_api()
        )
        self.assertEqual(result, "any data found")

    def test_retrieve_all_category_when_api_return_wrong_status(self):
        """
        test than function return an error message with the 
        status code if api return an error
        """
        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(500))
        result = (
            self.open_food_fact.retrieve_all_category_name_from_open_food_facts_api()
        )
        self.assertEqual(result, ("the server encounter an internal error", 500))

    def test_retrieve_food_with_url_category_is_ok(self):
        """
        test than function record the food in the db and create
        the relation with the category
        """
        open_food_facts.requests.get = MagicMock(
            return_value=MockResponseToApiForFood(200)
        )
        result = self.open_food_fact.retrieve_food_with_url_category(self.fake_cat)
        prod = Product.objects.all()[0]
        self.assertEqual(prod.product_name, "nutella")

    def test_retrieve_food_when_category_contain_any_food(self):
        """
        test than function return a message about any data from category
        """
        open_food_facts.requests.get = MagicMock(
            return_value=MockResponseToApi(200, True)
        )
        result = self.open_food_fact.retrieve_food_with_url_category(self.fake_cat)
        self.assertEqual(result, "any food contain in this category")

    def test_give_a_hyerarchi_score_to_category_of_product_is_ok(self):
        """
        test than function return a number
        """
        current_category = Category.objects.create(
            category_name="Pâtes à tartiner", url_category="https://eho_.com"
        )
        score = 4
        result = self.open_food_fact.give_a_hyerarchi_score_to_category_of_product(
            self.json_food, current_category
        )
        self.assertEqual(result, score)

    def test_give_hyerarchie_score_dont_match(self):
        """
        test than func return an error when category from list of category
        doesn t match with current category
        """
        current_category = Category.objects.create(
            category_name="category not exist", url_category="https://eho_.com"
        )
        result = self.open_food_fact.give_a_hyerarchi_score_to_category_of_product(
            self.json_food, current_category
        )
        self.assertEqual(result, 0)


class TestFood(TestCase):
    """
    class of test for all method of food class
    """

    def setUp(self):
        """
        init the data for all tests
        """
        range_int = [i for i in range(11)]
        range_letter = [i for i in string.ascii_letters][:4]
        self.product = Product.objects.create(
            id=12,
            product_name="invention",
            image_url="https://nutella.jpg",
            product_url="https://nutella.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="e",
        )

        self.best_product_ever = Product.objects.create(
            id=13,
            product_name="best product ever",
            image_url="https://best_product.jpg",
            product_url="https://best_product.com",
            fat=1.5,
            sugars=2.3366,
            saturated_fat=0.555,
            salt=10.234,
            nutriscore="a",
        )

        self.category = Category.objects.create(
            id=1,
            category_name="petit dej",
            url_category="https://petit_dej_au_lit.com"
        )
        self.category2 = Category.objects.create(
            id=2,
            category_name="petit dej2",
            url_category="https://petit_dej_au_lit.com2"
        )
        self.category3 = Category.objects.create(
            id=3,
            category_name="petit dej3",
            url_category="https://petit_dej_au_lit3.com"
        )
        self.category4 = Category.objects.create(
            id=4,
            category_name="petit dej4",
            url_category="https://petit_dej_au_lit4.com"
        )
        self.category5 = Category.objects.create(
            id=5,
            category_name="petit dej5",
            url_category="https://petit_dej_au_lit5.com"
        )
        self.category.products.add(self.product, through_defaults={
            'hyerarchie_score': 5
        })
        self.category2.products.add(self.product, through_defaults={
            'hyerarchie_score': 2
        })
        self.category3.products.add(self.product, through_defaults={
            'hyerarchie_score': 3
        })
        self.category4.products.add(self.product, through_defaults={
            'hyerarchie_score': 1
        })
        self.category5.products.add(self.product, through_defaults={
            'hyerarchie_score': 4
        })
        self.food = food.Food("invention")
        i = 0

        while i < 10:
            product = Product.objects.create(
                id=i,
                product_name=f"invention{i}",
                image_url=f"https://nutella{i}.jpg",
                product_url=f"https://nutella{i}.com",
                fat=random.choice(range_int),
                sugars=random.choice(range_int),
                saturated_fat=random.choice(range_int),
                salt=random.choice(range_int),
                nutriscore=random.choice(range_letter),
            )
            if product.nutriscore > "c":
                self.category.products.add(product, through_defaults={
                    'hyerarchie_score': 5
                })
                self.category2.products.add(product, through_defaults={
                    'hyerarchie_score': 2
                })

            self.category3.products.add(product, through_defaults={
                'hyerarchie_score': 3
            })
            i += 1

    def test_than_class_research_food_data_by_name_is_ok(self):
        """
        test than method search food by name retrieve food give in parameter
        with correct informations about it
        :product_name, nutriscore, fat, sugars, salt, saturated_fat,
        product_url, url_image, categories
        """
        result = self.food.search_food_and_categories_by_product_name()
        category_name = result.get("categories")[0].get("category_name")
        url_category = result.get("categories")[0].get("url_category")
        product_name = result.get("product").get("product_name")
        product_id = result.get("product").get("product_id")
        self.assertEqual(product_name, "invention")
        # self.assertEqual(product_id, 2)
        self.assertEqual(url_category, "https://petit_dej_au_lit.com")
        self.assertEqual(category_name, "petit dej")

    def test_search_food_and_categories_by_product_name_when_any_product_is_find(self):
        """
        test than function return an error message when any
        data is found
        """
        result = food.Food("nothing").search_food_and_categories_by_product_name()
        self.assertEqual(result, "product not found")

    def test_substitute_food_by_food_with_best_nutriscore_is_ok(self):
        """
        test than function return a list of food with the same
        category and a best nutriscore
        """
        complete_product = self.food.search_food_and_categories_by_product_name()
        nutriscore_of_complete_product = complete_product.get('product').get('nutriscore')
        result, commune_category = self.food.substitute_food_by_foods_with_best_nutriscore(
            complete_product
        )
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) <= 6)
        for substitute in result:
            self.assertTrue(substitute.get('nutriscore') <= nutriscore_of_complete_product)

    def test_substitute_food_by_food_with_best_nutriscore_wrong(self):
        """
        test the function when any best food is find
        """
        complete_best_product = food.Food(
            self.best_product_ever
        ).search_food_and_categories_by_product_name()
        result = self.food.substitute_food_by_foods_with_best_nutriscore(
            complete_best_product
        )
        self.assertEqual(result, ('this product have the best nutriscore', 'category commune'))

# endregion
