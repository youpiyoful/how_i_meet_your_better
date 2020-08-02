from django.test import TestCase
from .models import Product, Category
from business import open_food_facts
from unittest.mock import MagicMock
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
            self.error = 'the server encounter an internal error'

    def json(self):
        """
        response of api open food fact
        """
        if self.data_not_found:
            json_response = {
                "tags": []
            }

        else:
            json_response = {
                "tags": [
                    {
                        "url": "https://fake_url.com",
                        "name": "faux produit de test"
                    }
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
            self.error = 'the server encounter an internal error'

    def json(self):

        if self.data_not_found:
            json_response = {
                "products": []
            }

        else:
            json_response = {
                "products": [
                    {
                        'product_name': 'nutella',
                        'nutriscore_grade': 'd',
                        'url': 'https://nutella.com',
                        'nutriments': {
                            'fat': 10,
                            'saturated_fat': 15,
                            'sugars': 10,
                            'salt': 0.5
                        },
                        'image_url': 'htts://nutella.jpg',
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
        """
        self.open_food_fact = open_food_facts.OpenFoodFact()
        # create a fake category
        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(200))
        result = self.open_food_fact.retrieve_all_category_name_from_open_food_facts_api()
        self.fake_cat = Category.objects.all()[0]

    def test_than_retrieve_all_category_from_open_food_fact_is_ok(self):
        """
        test than function record the category in the db
        and return status 201
        """

        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(200))
        result = self.open_food_fact.retrieve_all_category_name_from_open_food_facts_api()
        cat = Category.objects.all()[0]
        self.assertNumQueries(1)
        self.assertEqual(result, 201)
        self.assertEqual(cat.url_category, 'https://fake_url.com')

    def test_retrieve_all_category_when_api_return_any_data(self):
        """
        test than function return 'any data found' when the api
        open food fact return nothing
        """
        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(200, True))
        result = self.open_food_fact.retrieve_all_category_name_from_open_food_facts_api()
        self.assertEqual(result, 'any data found')

    def test_retrieve_all_category_when_api_return_wrong_status(self):
        """
        test than function return an error message with the 
        status code if api return an error
        """
        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(500))
        result = self.open_food_fact.retrieve_all_category_name_from_open_food_facts_api()
        self.assertEqual(result, ('the server encounter an internal error', 500))

    def test_retrieve_food_with_url_category_is_ok(self):
        """
        test than function record the food in the db and create
        the relation with the category
        """
        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApiForFood(200))
        result = self.open_food_fact.retrieve_food_with_url_category(self.fake_cat)
        prod = Product.objects.all()[0]
        self.assertEqual(prod.product_name, 'nutella')

    def test_retrieve_food_when_category_contain_any_food(self):
        """
        test than function return a message about any data from category
        """
        open_food_facts.requests.get = MagicMock(return_value=MockResponseToApi(200, True))
        result = self.open_food_fact.retrieve_food_with_url_category(self.fake_cat)
        self.assertEqual(result, 'any food contain in this category')

# endregion