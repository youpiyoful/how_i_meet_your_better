"""
Test for the business app
"""
from django.test import TestCase
from .models import Product, Category
from django.shortcuts import reverse, get_object_or_404
from business import open_food_facts
from unittest.mock import MagicMock
import requests

# region TESTS OF VIEW
class IndexTests(TestCase):
    """
    test index view
    """
    def test_index_render_the_well_template(self):
        """
        test than '/' url return the index.html template
        and the correct context
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # find text contain for each block of code
        self.assertContains(response, 'Du gras, oui, mais de la qualité !', status_code=200)
        self.assertContains(response, 'Colette et Remy', status_code=200)
        self.assertContains(response, 'Contactez-nous !', status_code=200)


class ResultsTests(TestCase):
    """
    test the view results()
    """

    def setUp(self):
        """
        init the response for get request
        """
        self.response = self.client.get(reverse('business:results', kwargs={'product_name': 'nutella'}))

    def test_than_results_return_the_correct_context(self):
        """
        test than context contain all the data request
        by the user and render the correct template
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('nutriscore', self.response.context['foods_substitute'][0])
        self.assertIn('name', self.response.context['foods_substitute'][0])
        self.assertIn('category', self.response.context['foods_substitute'][0])
        self.assertIn('url_image', self.response.context['foods_substitute'][0])

    def test_the_list_of_food_substitute_contain_(self):
        """
        test than list of food substitute contain
        6 elements of food substitute
        """
        self.assertEqual(type(self.response.context['foods_substitute']), list)
        self.assertEqual(len(self.response.context['foods_substitute']), 6)

    def test_results_when_list_is_not_return(self):
        """
        when the list is not return the function
        provides an http404 exception
        """
        response = self.client.get('/himyb/results/empty')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Not Found', status_code=404)


class DetailFoodTests(TestCase):
    """
    test the view detail_food()
    """
    # def setUp(self):
    #     """
    #     create a product
    #     """
    #     Product(product_name="nutella")

    def test_detail_food_is_ok(self):
        """
        test than detail_food return the page detail food
        with element about substitute choose by the user
        """
        response = self.client.get(reverse('business:detail_food', kwargs={'food': 'nutella'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name', status_code=200)
        self.assertContains(response, 'nutriscore', status_code=200)


# class PageNotFound(TestCase):
#     """
#     test the personalize view 404 page not found
#     """
#     def test_render_page_not_found_is_ok(self):
#         """
#         test than view page not found render the well template
#         """
#         response = get_object_or_404(Product, product_name='coucou')
#         self.assertContains(response, '404 error', status_code=404)

# endregion


# region TEST OF MODELS
class ProductModelTests(TestCase):
    """
    test the product model
    """
    def test_str_function_return_the_product_name(self):
        """
        test the return of the product model
        """
        product = Product(product_name="pizza")
        self.assertEqual(str(product), product.product_name)


class CategoryModelTests(TestCase):
    """
    test the category model
    """
    def test_category_return_the_category_name(self):
        """
        test the return of the category model
        """
        category = Category(category_name="petit déjeuner")
        self.assertEqual(str(category), category.category_name)
# endregion


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